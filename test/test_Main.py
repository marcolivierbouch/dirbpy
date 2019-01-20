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
def test_GivenGetArgumentParser_ThenUrlArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-u')
    assert is_arg_in_parser_call(parser, '--url')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenOnlineArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-o')
    assert is_arg_in_parser_call(parser, '--online')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenVersionArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-v')
    assert is_arg_in_parser_call(parser, '--version')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenDirectoryArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-d')
    assert is_arg_in_parser_call(parser, '--directory')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenThreadArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-t')
    assert is_arg_in_parser_call(parser, '--thread')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenStatusCodeArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-c')
    assert is_arg_in_parser_call(parser, '--status_code')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenRemoveStatusCodeArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-r')
    assert is_arg_in_parser_call(parser, '--remove_status_code')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenProxyArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-p')
    assert is_arg_in_parser_call(parser, '--proxy')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenIgnoreStatusCodeArgumentIsAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-i')
    assert is_arg_in_parser_call(parser, '--ignore')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenNoDuplicateLogOptionAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '--no_duplicate')

@mock.patch('argparse.ArgumentParser')
def test_GivenGetArgumentParser_ThenNoDuplicateLogOptionAdded(argument_parser_mock):
    parser = get_parser()
    assert is_arg_in_parser_call(parser, '-s')
    assert is_arg_in_parser_call(parser, '--save')

def test_GivenArgumentParserRule_WhenNumberOfThreadIsToHigh_ThenErrorIsThrowed():
    try:
        number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST + 1)
    except:
        assert True
    else:
        assert False

def test_GivenArgumentParserRule_WhenNumberOfThreadEqualToMax_ThenNoErrorIsThrowed():
    try:
        number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST)
    except:
        assert False 
    else:
        assert True 

def test_GivenArgumentParserRule_WhenNumberOfThreadLessThanMax_ThenNoErrorIsThrowed():
    try:
        number_of_thread(URLBruteforcer.MAX_NUMBER_REQUEST - 1)
    except:
        assert False 
    else:
        assert True 

def test_GivenDictWithNone_WhenRemoveNoneValue_ThenNewDictWithNoNoneValueIsReturned():
    test_dict = {"first": None, "second": None, "third": 2}
    dict_with_no_none = remove_none_value_in_kwargs(test_dict)
    assert "third" in dict_with_no_none
    assert "first" not in dict_with_no_none
    assert "second" not in dict_with_no_none

def test_GivenGetParsedArgument_WhenFileOptionNotAdded_ThenProgramExitAndAskForFile():
    parser = get_parser()
    parser.error = MagicMock()
    args = get_parsed_args(parser, ['-u', 'test.com'])
    parser.error.assert_called_with(AnyStringWith('-f/--file'))

def test_GivenGetParsedArgument_WhenDirectoryOptionNotAdded_ThenProgramExitAndAskForDirectory():
    parser = get_parser()
    parser.error = MagicMock()
    args = get_parsed_args(parser, ['-u', 'test.com'])
    parser.error.assert_called_with(AnyStringWith('-d/--directory'))

def test_GivenGetParsedArgument_WhenOnlineFileOptionNotAdded_ThenProgramExitAndAskForOnlineFile():
    parser = get_parser()
    parser.error = MagicMock()
    args = get_parsed_args(parser, ['-u', 'test.com'])
    parser.error.assert_called_with(AnyStringWith('-o/--online'))
