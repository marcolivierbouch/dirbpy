#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import argparse
import glob
import logging

import requests

from _dirbpy.URLBruteforcer import URLBruteforcer
from _dirbpy.WordDictonary import WordDictonary
from _dirbpy.FileJSONFormatter import FileJSONFormatter
from _dirbpy import __version__, __author__

DIRBPY_COOL_LOOKING = '''
________   .__        ___.
\______ \  |__|_______\_ |__  ______  ___.__.
 |    |  \ |  |\_  __ \| __ \ \____ \<   |  |
 |    `   \|  | |  | \/| \_\ \|  |_> >\___  |
/_______  /|__| |__|   |___  /|   __/ / ____|
        \/                 \/ |__|    \/
'''

BLUE = "\033[1;34m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

NUMBER_OF_THREAD_PARAMETER_ERROR = 'The number of thread is to high. Current: {}, Max: {}'
GENERATED_WORD_MESSAGE = "Generated words: {}"

FORMAT = '{}[%(asctime)s]{} {}[%(levelname)s]{} %(message)s'.format(GREEN, RESET, BLUE, RESET)
logging.basicConfig(format=FORMAT, level=logging.INFO)
ROOT_LOGGER = logging.getLogger()


def remove_none_value_in_kwargs(params_dict: dict) -> dict:
    return {k: v for k, v in params_dict.items() if v is not None}


def do_request_with_online_file(dict_url: str, host: str, **kwargs) -> None:
    data = requests.get(dict_url)
    dict_list = str(data.content).replace('\\r', ' ').replace('\\n', ' ').split()
    use_url_bruteforcer(dict_list, host, **kwargs)


def do_request_with_dictionary(file_dict, host: str, **kwargs) -> None:
    word_dictionary = WordDictonary(file_dict)
    use_url_bruteforcer(word_dictionary, host, **kwargs)


def use_url_bruteforcer(words: list, host: str, **kwargs) -> None:
    params = remove_none_value_in_kwargs(kwargs) 
    ROOT_LOGGER.info(GENERATED_WORD_MESSAGE.format(len(words)))
    request_handler = URLBruteforcer(host, words, **params)
    request_handler.send_requests_with_all_words()


def number_of_thread(value: int) -> int:
    value = int(value)
    if value > URLBruteforcer.MAX_NUMBER_REQUEST:
        raise argparse.ArgumentTypeError(NUMBER_OF_THREAD_PARAMETER_ERROR.format(value, URLBruteforcer.MAX_NUMBER_REQUEST))
    return value


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        type=str,
                        help='This is the url to scan')
    parser.add_argument('-f', '--file',
                        type=str,
                        help='Input file with words.')
    parser.add_argument('-o', '--online',
                        type=str,
                        help='URL with raw dictionary')
    parser.add_argument('-d', '--directory',
                        type=str,
                        help='Input directory with dictionaries (.txt).')
    parser.add_argument('-t', '--thread',
                        type=number_of_thread,
                        help='Number of thread, the max value is {}'.format(URLBruteforcer.MAX_NUMBER_REQUEST))
    parser.add_argument('-c', '--status-code',
                        nargs='*',
                        type=int,
                        help='Status codes list to accept, the default list is: {}'.format(URLBruteforcer.VALID_STATUS_CODE))
    parser.add_argument('-r', '--remove-status-code',
                        nargs='*',
                        type=int,
                        help='Status codes list to remove from original list')
    parser.add_argument('-p', '--proxy',
                        nargs='*',
                        type=str,
                        help='Specify the url of the proxy if you want to use one. (Ex: localhost:8080)')
    parser.add_argument('-i', '--ignore',
                        nargs='*',
                        type=str,
                        help='Ignore a directory (Ex: css images)')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('--no-duplicate',
                        action='store_false',
                        help='Don\'t display duplicate logs')
    parser.add_argument('-s', '--save',
                        type=str,
                        help='Output file.')
    parser.add_argument('--hosts-file',
                        type=argparse.FileType('r'),
                        help='File with urls to scan')

    return parser


def get_parsed_args(parser, args):
    args_parsed = parser.parse_args(args)

    if not args_parsed.directory and not args_parsed.file and not args_parsed.online:
        parser.error('Need a file (-f/--file) or a directory (-d/--directory) or an online file (-o/--online) as input.')

    if not args_parsed.url and not args_parsed.hosts_file:
        parser.error('Need an url (-u/--url) or a hosts file (--hosts_file)')

    return args_parsed


def main():
    print(DIRBPY_COOL_LOOKING)
    print('Author: {}'.format(__author__))
    print('Version: {}\n'.format(__version__))
   
    parser = get_parser()
    args = get_parsed_args(parser, sys.argv[1:])

    proxy = args.proxy[0] if args.proxy else None

    status_code = None
    if args.status_code:
        status_code = args.status_code
    if args.remove_status_code:
        status_code = [code for code in URLBruteforcer.VALID_STATUS_CODE if code not in args.remove_status_code]

    directories_to_ignore = args.ignore
    dict_url = None
    if args.online:
        dict_url = args.online

    params = {
              "nb_thread": args.thread,
              "status_code": status_code,
              "proxy": proxy,
              "directories_to_ignore": directories_to_ignore,
              "duplicate_log": args.no_duplicate
             }

    if args.save:
        file_handler = logging.FileHandler(args.save)
        formatter = FileJSONFormatter()
        file_handler.setFormatter(formatter)
        ROOT_LOGGER.addHandler(file_handler)

    hosts = []
    if args.hosts_file:
        hosts = args.hosts_file.readlines()
        hosts = [host.rstrip('\n') for host in hosts]

    for host in hosts or [args.url]:
        if args.directory:
            for file in glob.glob("{}*.txt".format(args.directory if args.directory.endswith('/') else args.directory + '/')):
                ROOT_LOGGER.info('Current file: {}'.format(file))
                with open(file, 'r') as opened_file:
                    do_request_with_dictionary(opened_file, host, **params) 
        elif dict_url:
            do_request_with_online_file(dict_url, host, **params)
        else:
            with open(args.file, 'r') as opened_file:
                do_request_with_dictionary(opened_file, host, **params)

