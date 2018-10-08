#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from testfixtures import LogCapture
from unittest.mock import MagicMock
from unittest import mock

from _dirbpy.URLBruteforcer import URLBruteforcer, WordDictonary

HOST = 'http://localhost/'
WORD_LIST = ['css', 'js', 'test']

def test_Given_URLBruteforcer_When_ParmeterNbThreadIsNotSet_Then_DefaultValueIsUsed():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)
    params = {
        'status_code': [200],
        'proxy': {'http': None, 'https': None},
        'directories_to_ignore': [200]
    }
    url_bruteforcer = URLBruteforcer(HOST, word_dict, **params)
    assert url_bruteforcer.nb_thread == URLBruteforcer.MAX_NUMBER_REQUEST


def test_Given_URLBruteforcer_When_ParmeterStatusCodeListIsNotSet_Then_DefaultValueIsUsed():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)
    params = {
        'nb_thread': 1,
        'proxy': {'http': None, 'https': None},
        'directories_to_ignore': [200]
    }
    url_bruteforcer = URLBruteforcer(HOST, word_dict, **params)
    assert url_bruteforcer.status_code == URLBruteforcer.VALID_STATUS_CODE


def test_Given_URLBruteforcer_When_ParmeterProxyIsNotSet_Then_DefaultValueIsUsed():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)
    params = {
        'nb_thread': 1,
        'status_code': [200],
        'directories_to_ignore': [200]
    }
    url_bruteforcer = URLBruteforcer(HOST, word_dict, **params)
    assert url_bruteforcer.proxy == URLBruteforcer.PROXY_DEFAULT_DICT


def test_Given_URLBruteforcer_When_ParmeterDirectoryToIgnoreIsNotSet_Then_DefaultValueIsUsed():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)
    params = {
        'nb_thread': 1,
        'status_code': [200],
        'proxy': {'http': None, 'https': None}
    }
    url_bruteforcer = URLBruteforcer(HOST, word_dict, **params)
    assert url_bruteforcer.directories_to_ignore == [] 

@mock.patch('_dirbpy.URLBruteforcer.disable_https_warnings')
def test_Given_URLBruteforcer_When_URLHaveHtts_Then_WarningsAreDisable(disable_warnings_mock):
    disable_warnings_mock.return_value = True 
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)
    htts_host = 'https://localhost/'
    url_bruteforcer = URLBruteforcer(htts_host, word_dict)
    disable_warnings_mock.assert_called()

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_WordIsAnEmptyString_Then_WordIsNotUseToCompleteURL(get_mock):
    file_mock = MagicMock()
    words = ['']
    file_mock.readlines = MagicMock(return_value=words)
    word_dict = WordDictonary(file_mock)
    url_bruteforcer = URLBruteforcer(HOST, word_dict)
    url_bruteforcer.send_requests_with_all_words()
    assert False == get_mock.called

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_WordIsASlash_Then_WordIsNotUseToCompleteURL(get_mock):
    file_mock = MagicMock()
    words = ['/']
    file_mock.readlines = MagicMock(return_value=words)
    word_dict = WordDictonary(file_mock)
    url_bruteforcer = URLBruteforcer(HOST, word_dict)
    url_bruteforcer.send_requests_with_all_words()
    assert False == get_mock.called

@mock.patch('requests.get')
def test_Given_URLBruteforcer_When_RequestReturn200_Then_LoggerShowTheURL(get_mock):
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)
    url_bruteforcer = URLBruteforcer(HOST, word_dict)
    url_bruteforcer.send_requests_with_all_words()

def test_Given_URLBruteforcer_When_RequestReturn201_Then_LoggerShowTheURL():
    pass

def test_Given_URLBruteforcer_When_RequestReturn202_Then_LoggerShowTheURL():
    pass

def test_Given_URLBruteforcer_When_RequestReturn203_Then_LoggerShowTheURL():
    pass

def test_Given_URLBruteforcer_When_RequestReturn404ButHistoryHaveRequsest_Then_LoggerShowTheURLInHistory():
    pass

def test_Given_URLBruteforcer_When_RequestReturn404_Then_LoggerDontShowTheURL():
    pass

def test_Given_URLBruteforcer_When_RequestReturn200ButWasRedirection_Then_LoggerShowTheURLBeforeRedirection():
    pass

def test_Given_URLBruteforcer_When_RequestReturnURLThatEndWithSlash_Then_LoggerShowTheDirectory():
    pass

def test_Given_URLBruteforcer_When_RequestReturnADirectoryToIgnore_Then_BruterforcerDontRestart():
    pass

def test_Given_URLBruteforcer_When_RequestReturnURLThatEndWithSlash_Then_BruteforcerRestartWithNewUrl():
    pass

def test_Given_URLBruteforcer_When_RequestReturnNone_Then_TheNoneIsDiscardFromList():
    pass

def test_Given_URLBruteforcer_When_RequestReturnTheCurrentURL_Then_TheNoneIsDiscardFromList():
    pass

def test_Given_URLBruteforcer_When_RequestThrow_Then_ErrorIsCatchLoggerPrintError():
    pass
