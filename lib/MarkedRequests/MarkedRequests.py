import os
from urllib.parse import urlparse

import requests


_HEADER_MARKER = {"Skibidi": "toilet"}
_INVALID_IP = "-1.-1.-1.-1"


class _HeaderUpdateMixin:
    """Mixin to add specific headers if the hostname matches the vulnbox IP."""

    def __init__(self, vulnbox_ip: str | None = os.getenv('VM_IP', _INVALID_IP)):
        self.__vulnbox_ip = vulnbox_ip

    def update_headers(self, url, headers):
        """Update headers if the hostname matches the vulnbox IP."""
        headers = headers or {}
        if self.__vulnbox_ip == urlparse(url).hostname:
            headers.update(_HEADER_MARKER)
        return headers


class ADsession(requests.Session, _HeaderUpdateMixin):
    def __init__(self, vulnbox_ip: str | None = os.getenv('VM_IP', _INVALID_IP)):
        requests.Session.__init__(self)
        _HeaderUpdateMixin.__init__(self, vulnbox_ip)

    def get(self, url, params=None, headers=None, **kwargs):
        headers = self.update_headers(url, headers)
        return super().get(url, params=params, headers=headers, **kwargs)

    def post(self, url, params=None, headers=None, **kwargs):
        headers = self.update_headers(url, headers)
        return super().post(url, params=params, headers=headers, **kwargs)


class ADrequests(_HeaderUpdateMixin):
    def __init__(self, vulnbox_ip: str | None = os.getenv('VM_IP', _INVALID_IP)):
        super().__init__(vulnbox_ip)

    def get(self, url, params=None, headers=None, **kwargs):
        headers = self.update_headers(url, headers)
        return requests.get(url, params=params, headers=headers, **kwargs)

    def post(self, url, params=None, headers=None, **kwargs):
        headers = self.update_headers(url, headers)
        return requests.post(url, params=params, headers=headers, **kwargs)
