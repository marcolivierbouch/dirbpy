import json_log_formatter
from _dirbpy.URLBruteforcer import URLBruteforcer
import re

class FileJSONFormatter(json_log_formatter.JSONFormatter):

    TYPE_DIRECTORY = 'directory'
    TYPE_URL = 'url'

    def json_record(self, message, extra, record):
        if URLBruteforcer.SCANNING_URL_MESSAGE.split(':')[0] in message:
            extra['url'] = get_url_from_message(message)
        elif 'http' in message:
            extra['url'] = get_url_from_message(message)
            extra['status_code'] = get_status_code_from_message(message)
            extra['type'] = self.TYPE_DIRECTORY if 'Directory' in message else TYPE_URL
        else:
            extra['words_generated'] = get_number_of_word_generated_from_message(message)
        return extra

    def get_number_of_word_generated_from_message(message: str) -> int:
        pass

    def get_status_code_from_message(message: str) -> int:
        pass

    def get_url_from_message(message: str) -> str:
        m = re.search('(?:www|https|http?)[^\s]+', message)
        return m.group(0)
