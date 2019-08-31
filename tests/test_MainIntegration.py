# -*- coding: utf-8 -*-
import os
import sys
import subprocess

from pathlib import Path, PurePath

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PYTHON_EXEC = 'python'
DIRBPY_HELP_OPTION = ' --help'
BIN_DIRBPY_FILE = PurePath('dirbpy')
SRC_DIRBPY_FILE = PurePath('dirbpy.py')
BIN_FOLDER = PurePath('../bin')
SRC_FOLDER = PurePath('../src')

BIN_DIRBPY_PATH = DIR_PATH / BIN_FOLDER / BIN_DIRBPY_FILE
SRC_DIRBPY_PATH = DIR_PATH / SRC_FOLDER  / SRC_DIRBPY_FILE 


class TestCommandLine:
    

    def test_GivenShell_WhenAskForHelpToDirbpyInBinFolder_OutputIsNotEmpty(self):
        cmd = PYTHON_EXEC + ' ' + str(BIN_DIRBPY_PATH) + ' ' + DIRBPY_HELP_OPTION 

        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()

        assert 0 != len(output)
    

    def test_GivenShell_WhenAskForHelpToDirbpyInSrcFolder_OutputIsNotEmpty(self):
        cmd = PYTHON_EXEC + ' ' + str(SRC_DIRBPY_PATH) + ' ' + DIRBPY_HELP_OPTION 

        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()

        assert 0 != len(output)     
        
