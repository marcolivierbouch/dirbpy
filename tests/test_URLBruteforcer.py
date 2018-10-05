#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def Given_URLBruteforcer_When_ParmeterNbThreadIsNotSet_Then_DefaultValueIsUsed():
    pass

def Given_URLBruteforcer_When_ParmeterStatusCodeListIsNotSet_Then_DefaultValueIsUsed():
    pass

def Given_URLBruteforcer_When_ParmeterProxyIsNotSet_Then_DefaultValueIsUsed():
    pass

def Given_URLBruteforcer_When_ParmeterDirectoryToIgnoreIsNotSet_Then_DefaultValueIsUsed():
    pass

def Given_URLBruteforcer_When_URLHaveHtts_Then_WarningsAreDisable():
    pass

def Given_URLBruteforcer_When_WordIsAnEmptyString_Then_WordIsNotUseToCompleteURL():
    pass

def Given_URLBruteforcer_When_WordIsASlash_Then_WordIsNotUseToCompleteURL():
    pass

def Given_URLBruteforcer_When_RequestReturn200_Then_LoggerShowTheURL():
    pass

def Given_URLBruteforcer_When_RequestReturn201_Then_LoggerShowTheURL():
    pass

def Given_URLBruteforcer_When_RequestReturn202_Then_LoggerShowTheURL():
    pass

def Given_URLBruteforcer_When_RequestReturn203_Then_LoggerShowTheURL():
    pass

def Given_URLBruteforcer_When_RequestReturn404ButHistoryHaveRequsest_Then_LoggerShowTheURLInHistory():
    pass

def Given_URLBruteforcer_When_RequestReturn404_Then_LoggerDontShowTheURL():
    pass

def Given_URLBruteforcer_When_RequestReturn200ButWasRedirection_Then_LoggerShowTheURLBeforeRedirection():
    pass

def Given_URLBruteforcer_When_RequestReturnURLThatEndWithSlash_Then_LoggerShowTheDirectory():
    pass

def Given_URLBruteforcer_When_RequestReturnADirectoryToIgnore_Then_BruterforcerDontRestart():
    pass

def Given_URLBruteforcer_When_RequestReturnURLThatEndWithSlash_Then_BruteforcerRestartWithNewUrl():
    pass

def Given_URLBruteforcer_When_RequestReturnNone_Then_TheNoneIsDiscardFromList():
    pass

def Given_URLBruteforcer_When_RequestReturnTheCurrentURL_Then_TheNoneIsDiscardFromList():
    pass

def Given_URLBruteforcer_When_RequestThrow_Then_ErrorIsCatchLoggerPrintError():
    pass
