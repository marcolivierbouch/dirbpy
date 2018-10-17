#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import glob
import logging

import requests

from _dirbpy.URLBruteforcer import URLBruteforcer
from _dirbpy.WordDictonary import WordDictonary
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

FORMAT = '{}[%(asctime)s]{} {}[%(levelname)s]{} %(message)s'.format(GREEN, RESET, BLUE, RESET)
logging.basicConfig(format=FORMAT, level=logging.INFO)
ROOT_LOGGER = logging.getLogger()

def do_request_with_dictionary(file_dict, host: str, thread: int, status_code: list, proxy: str, directories_to_ignore: list) -> None:
    word_dictionary = WordDictonary(file_dict)
    ROOT_LOGGER.info('Generated words {}'.format(len(word_dictionary)))
    params = {}
    if thread:
        params['nb_thread'] = thread
    if status_code:
        params['status_code'] = status_code
    if proxy:
        params['proxy'] = proxy
    if directories_to_ignore:
        params['directories_to_ignore'] = directories_to_ignore

    request_handler = URLBruteforcer(host, word_dictionary, **params)
    request_handler.send_requests_with_all_words()

def number_of_thread(value) -> int:
    value = int(value)
    if value > URLBruteforcer.MAX_NUMBER_REQUEST:
        raise argparse.ArgumentError(NUMBER_OF_THREAD_PARAMETER_ERROR.format(value, URLBruteforcer.MAX_NUMBER_REQUEST))
    return value

def main():
    print(DIRBPY_COOL_LOOKING)
    print('Author: {}'.format(__author__))
    print('Version: {}\n'.format(__version__))
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        type=str,
                        required=True,
                        help='This is the url to scan')
    parser.add_argument('-f', '--file',
                        type=argparse.FileType('r'),
                        help='Input file with words.')
    parser.add_argument('-d', '--directory',
                        type=str,
                        help='Input directory with dictionary (.txt).')
    parser.add_argument('-t', '--thread',
                        type=number_of_thread,
                        help='Number of threads the max value is {}'.format(URLBruteforcer.MAX_NUMBER_REQUEST))
    parser.add_argument('-s', '--status_code',
                        nargs='*',
                        type=int,
                        help='list of status code to accept the default list is: {}'.format(URLBruteforcer.VALID_STATUS_CODE))
    parser.add_argument('-r', '--remove_status_code',
                        nargs='*',
                        type=int,
                        help='list of status code to remove from list')
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


    args = parser.parse_args()
    if not args.directory and not args.file:
        parser.error('Need a file (--file, -f) or a directory (--directory, -d) as input.')

    host = args.url
    proxy = args.proxy[0] if args.proxy else None

    status_code = None
    if args.status_code:
        status_code = args.status_code
    if args.remove_status_code:
        status_code = [code for code in status_code if code not in args.remove_status_code]

    directories_to_ignore = args.ignore
    if args.directory:
        for file in glob.glob("{}*.txt".format(args.directory if args.directory.endswith('/') else args.directory + '/')):
            ROOT_LOGGER.info('Current file: {}'.format(file))
            do_request_with_dictionary(open(file, 'r'), host, args.thread, status_code, proxy, directories_to_ignore)
    else:
        do_request_with_dictionary(args.file, host, args.thread, status_code, proxy, directories_to_ignore)


