import os
from urllib.parse import urlparse

import requests


class ADrequests(requests.Request):
    __INVALID_IP = "-1.-1.-1.-1"
    __HEADER_MARKER = {"Skibidi": "toilet"}
    __vulnbox_ip = ""

    def __init__(self, vulnbox_ip: str | None = os.getenv('VM_IP', __INVALID_IP)):
        super().__init__()
        self.__vulnbox_ip = urlparse(vulnbox_ip).hostname

    def get(self, url, params=None, headers=None, **kwargs):
        headers = {} if headers is None else headers

        if self.__vulnbox_ip == urlparse(url).hostname:
            headers.update(self.__HEADER_MARKER)

        return requests.get(url, params=params, headers=headers, **kwargs)

    def post(self, url, params=None, headers=None, **kwargs):
        headers = {} if headers is None else headers

        if self.__vulnbox_ip == urlparse(url).hostname:
            headers.update(self.__HEADER_MARKER)

        return requests.post(url, params=params, headers=headers, **kwargs)
