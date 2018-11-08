#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from unittest.mock import MagicMock

from _dirbpy.WordDictonary import WordDictonary

WORD_LIST = ['css', 'js', 'test']

def test_GivenWordDictionay_WhenItsGenerated_ThenTheFileInParameterIsRead():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)
    
    file_mock.readlines.assert_called()

def test_GivenWordDictionay_WhenItsGenerated_ThenCurrentIndexIsSetAtZero():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)
    word_dict = WordDictonary(file_mock)

    assert word_dict.current_index == 0

def test_GivenWordDictionay_WhenGetLength_ThenCurrentSizeIsReturned():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)

    word_dict = WordDictonary(file_mock)

    assert len(WORD_LIST) == len(word_dict)

def test_GivenWordDictionay_WhenIter_ThenAllWordAreReturned():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)

    word_dict = WordDictonary(file_mock)
    i = 0
    for word in word_dict:
        assert WORD_LIST[i] == word
        i += 1

def test_GivenWordDictionay_WhenIterSecondTime_ThenCurrentIndexIsSetAtZero():
    file_mock = MagicMock()
    file_mock.readlines = MagicMock(return_value=WORD_LIST)

    word_dict = WordDictonary(file_mock)
    [word for word in word_dict]
    word_dict.__iter__()
    assert word_dict.current_index == 0
