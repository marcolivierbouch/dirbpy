import json_log_formatter
import re

from _dirbpy.URLBruteforcer import URLBruteforcer

class FileJSONFormatter(json_log_formatter.JSONFormatter):

    TYPE_DIRECTORY = 'directory'
    TYPE_URL = 'url'
    
    SCAN_URL_KEY = 'scan_url'
    URL_KEY = 'url'
    ERROR_KEY = 'error'
    STATUS_CODE_KEY = 'status_code'
    TYPE_KEY = 'type'
    WORDS_GENERATED_KEY = 'words_generated'

    def json_record(self, message, extra, record):
        if URLBruteforcer.SCANNING_URL_MESSAGE.split(':')[0] in message:
            extra[self.SCAN_URL_KEY] = self.get_url_from_message(message)
        elif 'http' in message:
            extra[self.URL_KEY] = self.get_url_from_message(message)
            status_code = self.get_status_code_from_message(message)
            if status_code == message:
                extra[self.ERROR_KEY] = message
            else:   
                extra[self.STATUS_CODE_KEY] = status_code
                extra[self.TYPE_KEY] = self.TYPE_DIRECTORY if 'Directory' in message else self.TYPE_URL
        else:
            extra[self.WORDS_GENERATED_KEY] = self.get_number_of_word_generated_from_message(message)
        return extra

    def get_number_of_word_generated_from_message(self, message: str) -> str:
        no_muber_message = "Generated words: {}".format("")
        return message.replace(no_muber_message, '')

    def get_status_code_from_message(self, message: str) -> int or str:
        m = re.search(':\s(.*)', message)
        status_code = m.group(0).replace(')', '').replace(': ', '').replace(' ', '')
        try:
            return int(status_code)
        except ValueError:
            return (message)

    def get_url_from_message(self, message: str) -> str:
        m = re.search('(?:www|https|http?)[^\s]+', message)
        return m.group(0)
