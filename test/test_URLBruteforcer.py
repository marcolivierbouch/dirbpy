#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from unittest.mock import MagicMock
from unittest import mock

from _dirbpy.URLBruteforcer import URLBruteforcer

HOST = 'http://localhost/'
WORD_LIST = ['css', 'js', 'test']

def test_Given_URLBruteforcer_When_ParmeterNbThreadIsNotSet_Then_DefaultValueIsUsed():
    params = {
        'status_code': [200],
        'proxy': {'http': None, 'https': None},
        'directories_to_ignore': [200]
    }
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
    assert url_bruteforcer.nb_thread == URLBruteforcer.MAX_NUMBER_REQUEST


def test_Given_URLBruteforcer_When_ParmeterStatusCodeListIsNotSet_Then_DefaultValueIsUsed():
    params = {
        'nb_thread': 1,
        'proxy': {'http': None, 'https': None},
        'directories_to_ignore': [200]
    }
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
    assert url_bruteforcer.status_code == URLBruteforcer.VALID_STATUS_CODE


def test_Given_URLBruteforcer_When_ParmeterProxyIsNotSet_Then_DefaultValueIsUsed():
    params = {
        'nb_thread': 1,
        'status_code': [200],
        'directories_to_ignore': [200]
    }
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
    assert url_bruteforcer.proxy == URLBruteforcer.PROXY_DEFAULT_DICT


def test_Given_URLBruteforcer_When_ParmeterDirectoryToIgnoreIsNotSet_Then_DefaultValueIsUsed():
    params = {
        'nb_thread': 1,
        'status_code': [200],
        'proxy': {'http': None, 'https': None}
    }
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
    assert url_bruteforcer.directories_to_ignore == [] 

@mock.patch('_dirbpy.URLBruteforcer.disable_https_warnings')
def test_Given_URLBruteforcer_When_URLHaveHttps_Then_WarningsAreDisable(disable_warnings_mock):
    disable_warnings_mock.return_value = True 
    htts_host = 'https://localhost/'
    url_bruteforcer = URLBruteforcer(htts_host, WORD_LIST)
    disable_warnings_mock.assert_called()

@mock.patch('_dirbpy.URLBruteforcer.disable_https_warnings')
def test_Given_URLBruteforcer_When_URLDoesntHaveHttps_Then_WarningsAreNotDisable(disable_warnings_mock):
    disable_warnings_mock.return_value = True 
    htts_host = 'http://httpslocalhost/'
    url_bruteforcer = URLBruteforcer(htts_host, WORD_LIST)
    disable_warnings_mock.assert_not_called()

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_WordIsAnEmptyString_Then_WordIsNotUseToCompleteURL(get_mock):
    words = ['']
    url_bruteforcer = URLBruteforcer(HOST, words)
    url_bruteforcer.send_requests_with_all_words()
    assert False == get_mock.called

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_WordIsASlash_Then_WordIsNotUseToCompleteURL(get_mock):
    words = ['/']
    url_bruteforcer = URLBruteforcer(HOST, words)
    url_bruteforcer.send_requests_with_all_words()
    assert False == get_mock.called

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn200_Then_LoggerShowTheURL(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.history = None
    response_mock.url = 'https://localhost.com'
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.URL_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))

    get_mock.assert_called()
    logger_mock.info.assert_any_call(EXPECTED_LOG)


@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn201_Then_LoggerShowTheURL(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 201
    response_mock.history = None
    response_mock.url = 'https://localhost.com'
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.URL_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))

    get_mock.assert_called()
    logger_mock.info.assert_any_call(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn202_Then_LoggerShowTheURL(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 202
    response_mock.history = None
    response_mock.url = 'https://localhost.com'
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.URL_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))

    get_mock.assert_called()
    logger_mock.info.assert_any_call(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn203_Then_LoggerShowTheURL(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 203
    response_mock.history = None
    response_mock.url = 'https://localhost.com'
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.URL_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))

    get_mock.assert_called()
    logger_mock.info.assert_any_call(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn404ButHistoryHaveRequsest_Then_LoggerShowTheURLInHistory(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 404
    response_history_mock = mock.Mock()
    response_history_mock.status_code = 200
    response_mock.history = []
    response_mock.history.append(response_history_mock)
    response_mock.url = 'https://localhost.com/'
    get_mock.return_value = response_mock

    logger_mock = MagicMock()
    logger_mock.info = MagicMock()

    words = ['js'] 
    url_bruteforcer = URLBruteforcer(HOST, words, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.DIRECTORY_FOUND_MESSAGE.format(response_mock.url, str(response_history_mock.status_code))
    get_mock.assert_called()
    logger_mock.info.assert_any_call(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_StartScanningURL_Then_LoggerShowTheCurrentURL(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 404
    response_mock.history = []
    response_mock.url = HOST
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 

    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.SCANNING_URL_MESSAGE.format(HOST)
    get_mock.assert_called()
    logger_mock.info.assert_called_with(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn404_Then_LoggerDontShowTheURL(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 404
    response_mock.history = []
    response_mock.url = HOST
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 

    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.SCANNING_URL_MESSAGE.format(HOST)
    get_mock.assert_called()
    logger_mock.info.assert_called_once()
    logger_mock.info.assert_called_with(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn200ButWasRedirection_Then_LoggerShowTheURLBeforeRedirection(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_history_mock = mock.Mock()
    response_history_mock.status_code = 200
    response_history_mock.url = HOST
    response_mock.history = []
    response_mock.history.append(response_history_mock)
    response_mock.url = 'https://localhost.com/'
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 

    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.URL_FOUND_MESSAGE.format(response_history_mock.url, str(response_history_mock.status_code))
    get_mock.assert_called()
    logger_mock.info.assert_called_with(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturnURLThatEndWithSlash_Then_LoggerShowTheDirectory(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 301
    response_mock.history = []
    response_mock.url = 'https://localhost.com/'
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 

    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.DIRECTORY_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))
    get_mock.assert_called()
    logger_mock.info.assert_called_with(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturnADirectoryToIgnore_Then_BruterforcerDontRestart(get_mock):
    directory_to_ignore = ['js']

    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.history = None
    response_mock.url = 'https://localhost.com/{}/'.format(directory_to_ignore[0])
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    words = ['js']
    
    url_bruteforcer = URLBruteforcer(HOST, words, logger=logger_mock, directories_to_ignore=directory_to_ignore)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.DIRECTORY_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))
    get_mock.assert_called()
    logger_mock.info.assert_called_with(EXPECTED_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturnURLThatEndWithSlash_Then_BruteforcerRestartWithNewUrl(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.history = None
    response_mock.url = 'https://localhost.com/js/'
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    words = ['js']
    
    url_bruteforcer = URLBruteforcer(HOST, words, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.DIRECTORY_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))
    get_mock.assert_called()
    logger_mock.info.assert_called_with(EXPECTED_LOG)

    EXPECTED_RESTART_LOG = URLBruteforcer.SCANNING_URL_MESSAGE.format(response_mock.url)
    logger_mock.info.assert_any_call(EXPECTED_RESTART_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestADirectoryButUrlHaveDirectoryToIgnore_Then_BruterforcerRestart(get_mock):
    directory_to_ignore = ['js']

    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.history = None
    response_mock.url = 'https://{}localhost.com/css/'.format(directory_to_ignore[0])
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    words = ['js']
    
    url_bruteforcer = URLBruteforcer(HOST, words, logger=logger_mock, directories_to_ignore=directory_to_ignore)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.DIRECTORY_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))
    get_mock.assert_called()
    logger_mock.info.assert_called_with(EXPECTED_LOG)

    EXPECTED_RESTART_LOG = URLBruteforcer.SCANNING_URL_MESSAGE.format(response_mock.url)
    logger_mock.info.assert_any_call(EXPECTED_RESTART_LOG)

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturnNone_Then_TheNoneIsDiscardFromList(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 404
    response_mock.history = None
    response_mock.url = HOST 
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_RESTART_LOG = URLBruteforcer.SCANNING_URL_MESSAGE.format(HOST)
    logger_mock.info.assert_called_with(EXPECTED_RESTART_LOG)
    assert logger_mock.info.call_count == 1

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturnTheCurrentURL_Then_TheNoneIsDiscardFromList(get_mock):
    response_mock = mock.Mock()
    response_mock.status_code = 200
    response_mock.history = None
    response_mock.url = HOST 
    get_mock.return_value = response_mock

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    EXPECTED_LOG = URLBruteforcer.DIRECTORY_FOUND_MESSAGE.format(HOST, str(response_mock.status_code))
    logger_mock.info.assert_called_with(EXPECTED_LOG)

    EXPECTED_NOT_LOG = URLBruteforcer.SCANNING_URL_MESSAGE.format(HOST)
    assert EXPECTED_NOT_LOG not in logger_mock.info.call_args_list 

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestThrow_Then_ErrorIsCatchLoggerPrintError(get_mock):
    ERROR_MESSAGE = 'request get error'
    def raise_exception(url, proxies, verify):
        raise Exception(ERROR_MESSAGE)

    get_mock.side_effect = raise_exception 

    logger_mock = MagicMock() 
    logger_mock.info = MagicMock() 
    
    url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
    url_bruteforcer.send_requests_with_all_words()

    assert logger_mock.error.called
    logger_mock.error.assert_called_with(ERROR_MESSAGE)
