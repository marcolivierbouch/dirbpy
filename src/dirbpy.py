#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import glob
import logging

#  from dirbpy import URLBruteforcer, WordDictonary
#  import URLBruteforcer, WordDictonary
from _dirbpy.URLBruteforcer import URLBruteforcer
from _dirbpy.URLBruteforcer import WordDictonary
#  from src.dirbpy import URLBruteforcer

import requests

__version__ = '1.1.8'

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

if __name__ == "__main__":
    main()

#  def disable_https_warnings():
#      import urllib3
#      urllib3.disable_warnings()
#
#  class WordDictonary():
#
#      def __init__(self, word_dict):
#          self.words = word_dict.readlines()
#          self.current_index = 0
#
#      def __len__(self) -> int:
#          return len(self.words)
#
#      def __iter__(self):
#          self.current_index = 0
#          return self
#
#      def __next__(self) -> str:
#          if self.current_index == len(self.words):
#              raise StopIteration
#          value = self.words[self.current_index]
#          self.current_index += 1
#          return value.rstrip()
#
#
#  class URLBruteforcer():
#      MAX_NUMBER_REQUEST = 30
#      VALID_STATUS_CODE = [200, 201, 202, 203, 301, 302, 400, 401, 403, 405]
#      DIRECTORY_FOUND_MESSAGE = '++ Directory => {} (Status code: {})'
#      URL_FOUND_MESSAGE = '+ {} (Status code: {})'
#
#      proxy_default_dict = {'https': None, 'http': None}
#
#      def __init__(self, host: str,
#                   word_dictionary: WordDictonary,
#                   nb_thread: int = MAX_NUMBER_REQUEST,
#                   status_code: list = VALID_STATUS_CODE,
#                   proxy: dict = proxy_default_dict,
#                   directories_to_ignore: list = []):
#          self.host = host
#          if 'https' in self.host:
#              disable_https_warnings()
#          self.word_dictionary = word_dictionary
#          self.status_code = status_code
#          self.request_pool = ThreadPool(nb_thread)
#          self.proxy = proxy
#          self.directories_to_ignore = directories_to_ignore
#          self.logger = logging.getLogger(__name__)
#
#      def send_requests_with_all_words(self, url: str = None) -> None:
#          url = url or self.host
#          self.logger.info('Scanning URL: {}'.format(url))
#          url_completed = [urljoin(url, word) for word in self.word_dictionary if word not in ('/', '')]
#          directories_found = self.request_pool.map(self._request_thread, url_completed)
#          dir_with_no_none = self._remove_invalid_url_from_directory_found(directories_found, url)
#          for directory in dir_with_no_none:
#              if self._is_directory_to_ignore(directory):
#                  self.send_requests_with_all_words(directory)
#
#      def _is_directory_to_ignore(self, directory: str) -> bool:
#          return False if any([True for directories_to_ignore in self.directories_to_ignore if directories_to_ignore in directory]) else True
#
#      def _remove_invalid_url_from_directory_found(self, directories_found: list, url: str) -> list:
#          return [dir_to_test for dir_to_test in directories_found
#                  if dir_to_test is not None and dir_to_test != url]
#
#      def _request_thread(self, complete_url: str) -> str or None:
#          try:
#              response = requests.get(complete_url, proxies=self.proxy, verify=False)
#          except Exception as e:
#              self.logger.error(str(e))
#          else:
#              directory_url = None
#              if response.status_code in self.status_code:
#                  # We need to check for redirection if we are redirected we want the first url
#                  # Normaly get redirected it returns a 200 status_code but it not always the real status code
#                  if response.history and response.history[0].status_code in self.status_code:
#                      self.logger.info(self.URL_FOUND_MESSAGE.format(response.history[0].url, str(response.history[0].status_code)))
#                  elif response.url.endswith('/'):
#                      self.logger.info(self.DIRECTORY_FOUND_MESSAGE.format(response.url, str(response.status_code)))
#                      directory_url = response.url
#                  else:
#                      self.logger.info(self.URL_FOUND_MESSAGE.format(response.url, str(response.status_code)))
#              elif response.status_code == 404:
#                  # We need to check for redirection if we are redirected we want the first url
#                  # Normaly when we find a directory like /css/ it returns a 404
#                  if response.history and response.history[0].status_code in self.status_code:
#                      self.logger.info(self.DIRECTORY_FOUND_MESSAGE.format(response.url, str(response.history[0].status_code)))
#                      directory_url = response.url
#              return directory_url
#

