#!/usr/bin/env python
__author__ = 'shivangi'

import json
from collections import OrderedDict


class RequestReader(object):

    def __init__(self, json_file):
        self.json_file = json_file
        self._request = None

    def read_request(self):
        try:
            with open(self.json_file, "r") as fh:
                self._request = json.load(fp=fh, object_pairs_hook=OrderedDict)
        except Exception as err:
            raise err.__class__(err.message)

    def get_request(self, request_name=None):
        if not self._request:
            self.read_request()
            
        if not request_name:
            return self._request
        if self._request.has_key(request_name):
            return self._request[request_name]
        else:
            raise KeyError("No such request {0} exists".format(request_name))

    def validate_request(self, tags, index):
        sets_ = self._request
        while index:
            sets_ = getattr(sets_, 'values')()
            index -= 1
        flag = True
        for set_ in sets_:
            flag = True if set(set_.keys()).issuperset(set(tags)) else False
        return flag