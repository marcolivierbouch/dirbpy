#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pytest
import sys
sys.path.append('src')

from unittest.mock import MagicMock
from unittest import mock

from _dirbpy.__main__ import *
from _dirbpy.URLBruteforcer import URLBruteforcer

class AnyStringWith(str):
    def __eq__(self, other):
        return self in other

def is_arg_in_parser_call(parser, arg):
    url_added = False
    for call in parser.add_argument.call_args_list:
        if arg in call[0]:
            url_added = True
    return url_added


class TestArgumentParser:

    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenUrlArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-u')
        assert is_arg_in_parser_call(parser, '--url')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenOnlineArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-o')
        assert is_arg_in_parser_call(parser, '--online')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenVersionArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-v')
        assert is_arg_in_parser_call(parser, '--version')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenDirectoryArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-d')
        assert is_arg_in_parser_call(parser, '--directory')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenThreadArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-t')
        assert is_arg_in_parser_call(parser, '--thread')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenStatusCodeArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-c')
        assert is_arg_in_parser_call(parser, '--status-code')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenRemoveStatusCodeArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-r')
        assert is_arg_in_parser_call(parser, '--remove-status-code')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenProxyArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-p')
        assert is_arg_in_parser_call(parser, '--proxy')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenIgnoreStatusCodeArgumentIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-i')
        assert is_arg_in_parser_call(parser, '--ignore')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenNoDuplicateLogOptionAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '--no-duplicate')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenSaveOptionIsAdded(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '-s')
        assert is_arg_in_parser_call(parser, '--save')
    
    @mock.patch('argparse.ArgumentParser')
    def test_GivenArgumentParser_WhenGetArgumentParser_ThenReadHostFromFile(self, argument_parser_mock):
        parser = get_parser()
        assert is_arg_in_parser_call(parser, '--hosts-file')
    
    def test_GivenArgumentParserRule_WhenNumberOfThreadIsToHigh_ThenErrorIsThrowed(self):
        with pytest.raises(argparse.ArgumentTypeError):
            number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST + 1)
    
    def test_GivenArgumentParserRule_WhenNumberOfThreadEqualToMax_ThenNoErrorIsThrowed(self):
        try:
            number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST)
        except:
            assert False 
        else:
            assert True 
    
    def test_GivenArgumentParserRule_WhenNumberOfThreadLessThanMax_ThenNoErrorIsThrowed(self):
        try:
            number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST - 1)
        except:
            assert False 
        else:
            assert True 

    def test_GivenParsedArgument_WhenFileOptionNotAdded_ThenProgramExitAndAskForFile(self):
        parser = get_parser()
        parser.error = MagicMock()
        args = get_parsed_args(parser, ['-u', 'test.com'])
        parser.error.assert_called_with(AnyStringWith('-f/--file'))
    
    def test_GivenParsedArgument_WhenDirectoryOptionNotAdded_ThenProgramExitAndAskForDirectory(self):
        parser = get_parser()
        parser.error = MagicMock()
        args = get_parsed_args(parser, ['-u', 'test.com'])
        parser.error.assert_called_with(AnyStringWith('-d/--directory'))
    
    def test_GivenParsedArgument_WhenOnlineFileOptionNotAdded_ThenProgramExitAndAskForOnlineFile(self):
        parser = get_parser()
        parser.error = MagicMock()
        args = get_parsed_args(parser, ['-u', 'test.com'])
        parser.error.assert_called_with(AnyStringWith('-o/--online'))
    
    def test_GivenParsedArgument_WhenUrlOptionIsNotAdded_ThenProgramExitAndAskForUrl(self):
        parser = get_parser()
        parser.error = MagicMock()
        args = get_parsed_args(parser, ['-f', 'file.txt'])
        parser.error.assert_called_with(AnyStringWith('-u/--url'))

@mock.patch('requests.get')
def test_GivenMain_WhenDoRequestWithOnlineFile_ThenRequestGetIsCalled(get_mock):
    do_request_with_online_file('file', 'host')
    get_mock.assert_called()

@mock.patch('requests.get')
def test_GivenMain_WhenUseUrlBruteforce_ThenLoggerIsCalled(get_mock):
    ROOT_LOGGER.info = mock.Mock()
    use_url_bruteforcer('file', 'host')
    ROOT_LOGGER.info.assert_called()

def test_GivenDictWithNone_WhenRemoveNoneValue_ThenNewDictWithNoNoneValueIsReturned():
    test_dict = {"first": None, "second": None, "third": 2}
    dict_with_no_none = remove_none_value_in_kwargs(test_dict)
    assert "third" in dict_with_no_none
    assert "first" not in dict_with_no_none
    assert "second" not in dict_with_no_none

