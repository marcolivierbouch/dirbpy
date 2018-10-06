#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import logging

from urllib.parse import urljoin
from multiprocessing.dummy import Pool as ThreadPool

import requests

def disable_https_warnings():
    import urllib3
    urllib3.disable_warnings()

class WordDictonary():

    def __init__(self, file_word_dict):
        self.words = file_word_dict.readlines()
        self.current_index = 0

    def __len__(self) -> int:
        return len(self.words)

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self) -> str:
        if self.current_index == len(self.words):
            raise StopIteration
        value = self.words[self.current_index]
        self.current_index += 1
        return value.rstrip()


class URLBruteforcer():
    MAX_NUMBER_REQUEST = 30
    VALID_STATUS_CODE = [200, 201, 202, 203, 301, 302, 400, 401, 403, 405]
    DIRECTORY_FOUND_MESSAGE = '++ Directory => {} (Status code: {})'
    URL_FOUND_MESSAGE = '+ {} (Status code: {})'

    PROXY_DEFAULT_DICT = {'https': None, 'http': None}

    def __init__(self, host: str,
                 word_dictionary: list,
                 nb_thread: int = MAX_NUMBER_REQUEST,
                 status_code: list = VALID_STATUS_CODE,
                 proxy: dict = PROXY_DEFAULT_DICT,
                 directories_to_ignore: list = []):
        self.host = host
        if 'https' in self.host:
            disable_https_warnings()
        self.word_dictionary = word_dictionary
        self.status_code = status_code
        self.nb_thread = nb_thread
        self.request_pool = ThreadPool(self.nb_thread)
        self.proxy = proxy
        self.directories_to_ignore = directories_to_ignore
        self.logger = logging.getLogger(__name__)

    def send_requests_with_all_words(self, url: str = None) -> None:
        url = url or self.host
        self.logger.info('Scanning URL: {}'.format(url))
        url_completed = [urljoin(url, word) for word in self.word_dictionary if word not in ('/', '')]
        directories_found = self.request_pool.map(self.request_thread, url_completed)
        dir_filtered = self._remove_invalid_url_from_directory_found(directories_found, url)
        for directory in dir_filtered:
            if not self._is_directory_to_ignore(directory):
                self.send_requests_with_all_words(directory)

    def _is_directory_to_ignore(self, directory: str) -> bool:
        directory_found_to_ignore = [True for directory_to_ignore in self.directories_to_ignore 
                                    if directory_to_ignore in directory]
        return True if any(directory_found_to_ignore) else False

    def _remove_invalid_url_from_directory_found(self, directories_found: list, url: str) -> list:
        return [dir_to_test for dir_to_test in directories_found 
                if dir_to_test is not None and dir_to_test != url]

    def request_thread(self, complete_url: str) -> str or None:
        try:
            response = requests.get(complete_url, proxies=self.proxy, verify=False)
        except Exception as e:
            self.logger.error(str(e))
        else:
            return self.analyse_response(response)
            
    def analyse_response(self, response) -> str or None:
        directory_url = None
        if response.status_code in self.status_code:
            # We need to check for redirection if we are redirected we want the first url
            # Normaly get redirected it returns a 200 status_code but it not always the real status code
            if response.history and response.history[0].status_code in self.status_code:
                self.logger.info(self.URL_FOUND_MESSAGE.format(response.history[0].url, str(response.history[0].status_code)))
            elif response.url.endswith('/'):
                self.logger.info(self.DIRECTORY_FOUND_MESSAGE.format(response.url, str(response.status_code)))
                directory_url = response.url
            else:
                self.logger.info(self.URL_FOUND_MESSAGE.format(response.url, str(response.status_code)))
        elif response.status_code == 404:
            # We need to check for redirection if we are redirected we want the first url
            # Normaly when we find a directory like /css/ it returns a 404
            if response.history and response.history[0].status_code in self.status_code:
                self.logger.info(self.DIRECTORY_FOUND_MESSAGE.format(response.url, str(response.history[0].status_code)))
                directory_url = response.url
        return directory_url

