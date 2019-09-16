#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from unittest.mock import MagicMock
from unittest import mock

from _dirbpy.URLBruteforcer import URLBruteforcer

HOST = 'http://localhost.com/'
WORD_LIST = ['css', 'js', 'test']


class fakeRecord:
    def __init__(self, msg):
        self.msg = msg


class TestURLBruteforcer:

    def test_GivenURLBruteforcer_WhenParmeterNbThreadIsNotSet_ThenDefaultValueIsUsed(self):
        params = {
            'status_code': [200],
            'proxy': {'http': None, 'https': None},
            'directories_to_ignore': [200]
        }
        url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
        assert url_bruteforcer.nb_thread == URLBruteforcer.MAX_NUMBER_REQUEST
    
    
    def test_GivenURLBruteforcer_WhenParmeterStatusCodeListIsNotSet_ThenDefaultValueIsUsed(self):
        params = {
            'nb_thread': 1,
            'proxy': {'http': None, 'https': None},
            'directories_to_ignore': [200]
        }
        url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
        assert url_bruteforcer.status_code == URLBruteforcer.VALID_STATUS_CODE
    
    
    def test_GivenURLBruteforcer_WhenParmeterProxyIsNotSet_ThenDefaultValueIsUsed(self):
        params = {
            'nb_thread': 1,
            'status_code': [200],
            'directories_to_ignore': [200]
        }
        url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
        assert url_bruteforcer.proxy == URLBruteforcer.PROXY_DEFAULT_DICT
    
    
    def test_GivenURLBruteforcer_WhenParmeterDirectoryToIgnoreIsNotSet_ThenDefaultValueIsUsed(self):
        params = {
            'nb_thread': 1,
            'status_code': [200],
            'proxy': {'http': None, 'https': None}
        }
        url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, **params)
        assert url_bruteforcer.directories_to_ignore == [] 
    
    @mock.patch('_dirbpy.URLBruteforcer.disable_https_warnings')
    def test_GivenURLBruteforcer_WhenURLHaveHttps_ThenWarningsAreDisable(self, disable_warnings_mock):
        disable_warnings_mock.return_value = True 
        htts_host = 'https://localhost/'
        url_bruteforcer = URLBruteforcer(htts_host, WORD_LIST)
        disable_warnings_mock.assert_called()
    
    @mock.patch('_dirbpy.URLBruteforcer.disable_https_warnings')
    def test_GivenURLBruteforcer_WhenURLDoesntHaveHttps_ThenWarningsAreNotDisable(self, disable_warnings_mock):
        disable_warnings_mock.return_value = True 
        htts_host = 'http://httpslocalhost/'
        url_bruteforcer = URLBruteforcer(htts_host, WORD_LIST)
        disable_warnings_mock.assert_not_called()
    
    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenWordIsAnEmptyString_ThenWordIsNotUseToCompleteURL(self, get_mock):
        words = ['']
        url_bruteforcer = URLBruteforcer(HOST, words)
        url_bruteforcer.send_requests_with_all_words()
        assert False == get_mock.called
    
    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenWordIsASlash_ThenWordIsNotUseToCompleteURL(self, get_mock):
        words = ['/']
        url_bruteforcer = URLBruteforcer(HOST, words)
        url_bruteforcer.send_requests_with_all_words()
        assert False == get_mock.called

    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenCreatedWithProxy_ThenGetIsCalledWithProxy(self, get_mock):
        words = ['js']
        current_proxy = URLBruteforcer.PROXY_DEFAULT_DICT
        current_proxy[URLBruteforcer.HTTP_STR] = 'http://localhost'
        current_proxy[URLBruteforcer.HTTPS_STR] = 'https://localhost'

        url_bruteforcer = URLBruteforcer(HOST, words, proxy=current_proxy)
        url_bruteforcer.send_requests_with_all_words()

        assert current_proxy == get_mock.call_args_list[0][1]['proxies']
    
    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenRequestReturns200_ThenLoggerShowTheURL(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturns201_ThenLoggerShowTheURL(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturns202_ThenLoggerShowTheURL(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturns203_ThenLoggerShowTheURL(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturns404ButHistoryHasRequest_ThenLoggerShowTheURLInHistory(self, get_mock):
        response_mock = mock.Mock()
        response_mock.status_code = 404
        response_history_mock = mock.Mock()
        response_history_mock.status_code = 200
        response_mock.history = [response_history_mock]
        response_mock.url = 'https://localhost.com/js/'
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
    def test_GivenURLBruteforcer_WhenRequestReturnsValidStatusCodeAndHasHistoryWithInvalidStatusCode_ThenLoggerDoesntShowTheHistoryURL(self, get_mock):
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_history_mock = mock.Mock()
        response_history_mock.status_code = 404
        response_history_mock.url = 'https://localhost.com/html'
        response_mock.history = [response_history_mock]
        response_mock.url = 'https://localhost.com/js'
        get_mock.return_value = response_mock
    
        logger_mock = MagicMock()
        logger_mock.info = MagicMock()
    
        words = ['js'] 
        url_bruteforcer = URLBruteforcer(HOST, words, logger=logger_mock)
        url_bruteforcer.send_requests_with_all_words()
    
        UNEXPECTED_LOG = URLBruteforcer.URL_FOUND_MESSAGE.format(response_history_mock.url, str(response_history_mock.status_code))
        get_mock.assert_called()
        for call in logger_mock.info.mock_calls:
            assert call.call_args_list != [UNEXPECTED_LOG]
    
    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenStartScanningURL_ThenLoggerShowTheCurrentURL(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturns404_ThenLoggerDontShowTheURL(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturns200ButWasRedirection_ThenLoggerShowTheURLBeforeRedirection(self, get_mock):
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_history_mock = mock.Mock()
        response_history_mock.status_code = 200
        response_history_mock.url = HOST
        response_mock.history = [response_history_mock]
        response_mock.url = HOST 
        get_mock.return_value = response_mock
    
        logger_mock = MagicMock() 
        logger_mock.info = MagicMock() 
    
        url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
        url_bruteforcer.send_requests_with_all_words()
    
        EXPECTED_LOG = URLBruteforcer.URL_FOUND_MESSAGE.format(response_history_mock.url, str(response_history_mock.status_code))
        get_mock.assert_called()
        logger_mock.info.assert_any_call(EXPECTED_LOG)
    
    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenRequestReturnss301ButWasRedirectionAndRemovedSlash_ThenLoggerShowTheDirectoryURL(self, get_mock):
        response_mock = mock.Mock()
        response_mock.status_code = 301
        response_history_mock = mock.Mock()
        response_history_mock.status_code = 200
        response_history_mock.url = HOST + 'css'
        response_mock.history = [response_history_mock]
        response_mock.url = HOST + 'css/'
        get_mock.return_value = response_mock
    
        logger_mock = MagicMock() 
        logger_mock.info = MagicMock() 
    
        url_bruteforcer = URLBruteforcer(HOST, WORD_LIST, logger=logger_mock)
        url_bruteforcer.send_requests_with_all_words()
    
        EXPECTED_LOG = URLBruteforcer.DIRECTORY_FOUND_MESSAGE.format(response_mock.url, str(response_mock.status_code))
        get_mock.assert_called()
        logger_mock.info.assert_any_call(EXPECTED_LOG)
    
    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenRequestReturnsURLThatEndWithSlash_ThenLoggerShowTheDirectory(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturnssADirectoryToIgnore_ThenBruterforcerDontRestart(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturnssURLThatEndsWithSlash_ThenBruteforcerRestartWithNewUrl(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestADirectoryButUrlHasDirectoryToIgnore_ThenBruterforcerRestart(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturnsNone_ThenTheNoneIsDiscardFromList(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestReturnsTheCurrentURL_ThenTheCurrentURLIsDiscardFromList(self, get_mock):
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
    def test_GivenURLBruteforcer_WhenRequestThrow_ThenErrorIsCatchLoggerPrintError(self, get_mock):
        ERROR_MESSAGE = 'request get error'
        def raise_exception(url, proxies, verify):
            raise Exception(ERROR_MESSAGE)
    
        get_mock.side_effect = raise_exception 
    
        logger_mock = MagicMock() 
        logger_mock.info = MagicMock() 
        
        word_list = ['css']
        url_bruteforcer = URLBruteforcer(HOST, word_list, logger=logger_mock)
        url_bruteforcer.send_requests_with_all_words()
    
        assert logger_mock.error.called
        logger_mock.error.assert_called_with(ERROR_MESSAGE + '. URL: ' + HOST + word_list[0], exc_info=True)
    
    def test_GivenURLBruteforcer_WhenNotLoggingDuplicate_ThenAddFilterIsCalled(self):
        logger_mock = MagicMock() 
        logger_mock.info = MagicMock() 
    
        word_list = ['css']
        args = {"logger": logger_mock, "duplicate_log": False}
        url_bruteforcer = URLBruteforcer(HOST, word_list, **args)
    
        assert logger_mock.addFilter.assert_called
    
    def test_GivenURLBruteforcer_WhenNotLoggingDuplicate_ThenListOfLoggedMessageIsSet(self):
        logger_mock = MagicMock() 
        logger_mock.info = MagicMock() 
    
        word_list = ['css']
        args = {"logger": logger_mock, "duplicate_log": False}
        url_bruteforcer = URLBruteforcer(HOST, word_list, **args)
    
        assert hasattr(url_bruteforcer, 'logged_message')
    
    @mock.patch('requests.get')
    def test_GivenURLBruteforcer_WhenNotLoggingDuplicate_ThenFilterShouldNotDisplaySameMsg(self, get_mock):
        logger_mock = MagicMock() 
        logger_mock.info = MagicMock() 
    
        word_list = ['css']
        args = {"logger": logger_mock, "duplicate_log": False}
        url_bruteforcer = URLBruteforcer(HOST, word_list, **args)
        record = fakeRecord("msg")
        assert url_bruteforcer.no_duplicate_log_filter(record)
        assert not url_bruteforcer.no_duplicate_log_filter(record)

