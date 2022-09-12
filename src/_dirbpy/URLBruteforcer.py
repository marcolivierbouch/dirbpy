# -*- coding: utf-8 -*-

import glob
import logging
import difflib
import requests

from logging import Logger
from urllib.parse import urljoin, urlparse
from multiprocessing.dummy import Pool as ThreadPool


def disable_https_warnings():
    import urllib3
    urllib3.disable_warnings()

class URLBruteforcer():
    HTTPS_STR = 'https'
    HTTP_STR = 'http'
    MAX_NUMBER_REQUEST = 30
    VALID_STATUS_CODE = [200, 201, 202, 203, 301, 302, 400, 401, 403, 405, 500, 503]
    DIRECTORY_FOUND_MESSAGE = 'Directory => {} (Status code: {})'
    URL_FOUND_MESSAGE = '{} (Status code: {})'
    SCANNING_URL_MESSAGE = 'Scanning URL: {}'
    PROXY_DEFAULT_DICT = {HTTPS_STR: None, HTTP_STR: None}

    def __init__(self, host:            str,
                 word_dictionary:       list,
                 nb_thread:             int    = MAX_NUMBER_REQUEST,
                 status_code:           list   = VALID_STATUS_CODE,
                 proxy:                 dict   = PROXY_DEFAULT_DICT,
                 cookies:               dict   = {},
                 directories_to_ignore: list   = [],
                 logger:                Logger = logging.getLogger(__name__),
                 duplicate_log:         bool   = True):
        
        self.cookies = cookies
        self.host = host
        if 'https' in urlparse(self.host).scheme:
            disable_https_warnings()
        self.word_dictionary = word_dictionary
        self.status_code = status_code
        self.nb_thread = nb_thread
        self.request_pool = ThreadPool(self.nb_thread)

        if proxy == self.PROXY_DEFAULT_DICT:
            self.proxy = proxy
        else:
            self.proxy = self.PROXY_DEFAULT_DICT
            self.proxy[self.HTTPS_STR] = self._url_to_https(proxy)
            self.proxy[self.HTTP_STR] = self._url_to_http(proxy)
        self.directories_to_ignore = directories_to_ignore
        self.logger = logger
        if not duplicate_log:
            self.logged_message = []
            self.logger.addFilter(self.no_duplicate_log_filter)

    def no_duplicate_log_filter(self, record) -> bool:
        if record.msg not in self.logged_message:
            self.logged_message.append(record.msg)
            return True
        return False

    def send_requests_with_all_words(self, url: str = None) -> None:
        url = url or self.host
        self.logger.info(self.SCANNING_URL_MESSAGE.format(url))
        url_completed = self._generate_complete_url_with_word(url)
        directories_found = self.request_pool.map(self._request_thread, url_completed)
        flat_list_of_directories = self._generate_fat_list_with_list_of_list(directories_found)
        dir_filtered = self._remove_invalid_url_from_directory_found(flat_list_of_directories, url)
        for directory in dir_filtered:
            if not self._is_directory_to_ignore(directory):
                self.send_requests_with_all_words(directory)

    def _url_to_https(self, url: str) -> str:
        return url.replace(self.HTTP_STR, self.HTTPS_STR)

    def _url_to_http(self, url: str) -> str:
        return url.replace(self.HTTPS_STR, self.HTTP_STR)
   
    def _generate_fat_list_with_list_of_list(self, list_of_list: list) -> list:
        return [item for sublist in list_of_list for item in sublist]

    def _generate_complete_url_with_word(self, url: str) -> list:
        return [urljoin(url, word) for word in self.word_dictionary if word not in ('/', '')]

    def _is_directory_to_ignore(self, directory: str) -> bool:
        directory_found_to_ignore = [True for directory_to_ignore in self.directories_to_ignore 
                                     if directory_to_ignore in urlparse(directory).path]
        return True if any(directory_found_to_ignore) else False

    def _remove_invalid_url_from_directory_found(self, directories_found: list, url: str) -> list:
        return [dir_to_test for dir_to_test in directories_found 
                if dir_to_test is not None and dir_to_test != url]

    def _request_thread(self, complete_url: str) -> list:
        try:
            response = requests.get(complete_url, proxies=self.proxy, verify=False, cookies=self.cookies)
        except Exception as e:
            self.logger.error(str(e) + '. URL: {}'.format(complete_url), exc_info=True)
            return []
        else:
            return self._analyse_response(response)
            
    def _response_has_valid_status_code(self, response) -> bool:
        return response.status_code in self.status_code

    def _analyse_response(self, response) -> list:
        directories_url_found = []
        if self._response_has_valid_status_code(response):
            # We need to check for redirection, if we are redirected we want the first url
            # Normaly get redirected it returns a 200 status_code but it not always the real status code
            if response.history:
                for response_in_history in response.history:
                    # Check if it's the same path
                    response_removed_url = response.url.replace(response_in_history.url, '')
                    if response_removed_url == '/':
                        self.logger.info(self.DIRECTORY_FOUND_MESSAGE.format(response.url, str(response.status_code)))
                        directories_url_found.append(response.url)
                    else:
                        # Sometimes the response contains invalid status code
                        if self._response_has_valid_status_code(response_in_history):
                            self.logger.info(self.URL_FOUND_MESSAGE.format(response_in_history.url, str(response_in_history.status_code)))

            # Analyse the response if we didn't print it earlier
            if response.url not in directories_url_found:
                if response.url.endswith('/'): 
                    self.logger.info(self.DIRECTORY_FOUND_MESSAGE.format(response.url, str(response.status_code)))
                    directories_url_found.append(response.url)
                else:
                    self.logger.info(self.URL_FOUND_MESSAGE.format(response.url, str(response.status_code)))
        elif response.status_code == 404:
            # We need to check for redirection if we are redirected we want the first url
            # Normaly when we find a directory like /css/ it returns a 404
            if response.history and response.history[0].status_code in self.status_code:
                if response.url.endswith('/'):
                    self.logger.info(self.DIRECTORY_FOUND_MESSAGE.format(response.url, str(response.history[0].status_code)))
                    directories_url_found.append(response.url)
        return directories_url_found

