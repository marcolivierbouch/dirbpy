#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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


