#!/bin/false
import requests
import os

## use this in scripts
# import requests
# from adrequests import *
class Adrequests:
#    def __init__(self):
#        super()
#        self._orig_get = self.get
#        self.get = self._new_get

    def get(url, params=None, headers=None, vm_ip=None, **kwargs):
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :param vm_ip: (optional) ip of the vulnbox to check against url
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        if vm_ip is None:
            vm_ip = os.getenv('VM_IP', None)

        if vm_ip and vm_ip in url.split('/')[2]:
            if headers is not None:
                if 'skibidi' in headers.keys():
                    headers['skibidi'] = 'toilet'
            else:
                    headers = {}
                    headers['skibidi'] = 'toilet'

        return requests.get(url, params=params, headers=headers, **kwargs)
