#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from unittest.mock import MagicMock

from _dirbpy.WordDictonary import WordDictonary

WORD_LIST = ['css', 'js', 'test']


class TestWordDictionary:

    def test_GivenWordDictionary_WhenItsGenerated_ThenTheFileInParameterIsRead(self):
        file_mock = MagicMock()
        file_mock.readlines = MagicMock(return_value=WORD_LIST)
        word_dict = WordDictonary(file_mock)
        
        file_mock.readlines.assert_called()
    
    def test_GivenWordDictionary_WhenItsGenerated_ThenCurrentIndexIsSetAtZero(self):
        file_mock = MagicMock()
        file_mock.readlines = MagicMock(return_value=WORD_LIST)
        word_dict = WordDictonary(file_mock)
    
        assert word_dict.current_index == 0
    
    def test_GivenWordDictionary_WhenGetLength_ThenCurrentSizeIsReturned(self):
        file_mock = MagicMock()
        file_mock.readlines = MagicMock(return_value=WORD_LIST)
    
        word_dict = WordDictonary(file_mock)
    
        assert len(WORD_LIST) == len(word_dict)
    
    def test_GivenWordDictionary_WhenIter_ThenAllWordAreReturned(self):
        file_mock = MagicMock()
        file_mock.readlines = MagicMock(return_value=WORD_LIST)
    
        word_dict = WordDictonary(file_mock)
        i = 0
        for word in word_dict:
            assert WORD_LIST[i] == word
            i += 1
    
    def test_GivenWordDictionary_WhenIterSecondTime_ThenCurrentIndexIsSetAtZero(self):
        file_mock = MagicMock()
        file_mock.readlines = MagicMock(return_value=WORD_LIST)
    
        word_dict = WordDictonary(file_mock)
        [word for word in word_dict]
        word_dict.__iter__()
        assert word_dict.current_index == 0

