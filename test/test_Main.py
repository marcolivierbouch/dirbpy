#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from unittest.mock import MagicMock
from unittest import mock

from _dirbpy.main import *
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

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_UrlArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-u')
    assert is_arg_in_parser_call(parser, '--url')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_OnlineArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-o')
    assert is_arg_in_parser_call(parser, '--online')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_VersionArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-v')
    assert is_arg_in_parser_call(parser, '--version')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_DirectoryArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-d')
    assert is_arg_in_parser_call(parser, '--directory')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_ThreadArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-t')
    assert is_arg_in_parser_call(parser, '--thread')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_StatusCodeArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-s')
    assert is_arg_in_parser_call(parser, '--status_code')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_RemoveStatusCodeArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-r')
    assert is_arg_in_parser_call(parser, '--remove_status_code')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_ProxyArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-p')
    assert is_arg_in_parser_call(parser, '--proxy')

@mock.patch('argparse.ArgumentParser')
def test_Given_getArgumentParser_Then_IgnoreStatusCodeArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-i')
    assert is_arg_in_parser_call(parser, '--ignore')

def test_Given_ArgumentParserRule_When_NumberOfThreadIsToHigh_Then_ErrorIsThrowed():
    try:
        number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST + 1)
    except:
        assert True
    else:
        assert False

def test_Given_ArgumentParserRule_When_NumberOfThreadEqualToMax_Then_NoErrorIsThrowed():
    try:
        number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST)
    except:
        assert False 
    else:
        assert True 

def test_Given_ArgumentParserRule_When_NumberOfThreadLessThanMax_Then_NoErrorIsThrowed():
    try:
        number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST - 1)
    except:
        assert False 
    else:
        assert True 

def test_Given_DictWithNone_When_RemoveNoneValue_Then_NewDictWithNoNoneValueIsReturned():
    test_dict = {"first": None, "second": None, "third": 2}
    dict_with_no_none = remove_none_value_in_kwargs(test_dict)
    assert "third" in dict_with_no_none
    assert "first" not in dict_with_no_none
    assert "second" not in dict_with_no_none

def test_Given_getParsedArgument_When_NotFileOptionAdded_Then_ProgramExitAndAskForFile():
    parser = get_parser()
    parser.error = MagicMock()
    args = get_parsed_args(parser, ['-u', 'test.com'])
    parser.error.assert_called_with(AnyStringWith('-f/--file'))

def test_Given_getParsedArgument_When_NotFileOptionAdded_Then_ProgramExitAndAskForDirectory():
    parser = get_parser()
    parser.error = MagicMock()
    args = get_parsed_args(parser, ['-u', 'test.com'])
    parser.error.assert_called_with(AnyStringWith('-d/--directory'))

def test_Given_getParsedArgument_When_NotFileOptionAdded_Then_ProgramExitAndAskForOnlineFile():
    parser = get_parser()
    parser.error = MagicMock()
    args = get_parsed_args(parser, ['-u', 'test.com'])
    parser.error.assert_called_with(AnyStringWith('-o/--online'))
