#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from unittest.mock import MagicMock
from unittest import mock

from _dirbpy.FileJSONFormatter import FileJSONFormatter

def test_GivenMessage_WhenGetURLWithHTTPFromMessage_ThenURLIsReturned():
    url = "http://mysite.dirbpy"
    message = "Scanning url: {}".format(url)
    actual_url = FileJSONFormatter.get_url_from_message(message)
    assert url == actual_url
