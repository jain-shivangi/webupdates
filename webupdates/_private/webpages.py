#!/usr/bin/env python
__author__ = 'shivangi'

import os
import re
import requests


if hasattr(requests.packages.urllib3, 'disable_warnings'):
    requests.packages.urllib3.disable_warnings()


def store_back_output(path, mode="w+"):
    def outer_decorator(func):
        def inner_decorator(*args, **kwargs):
            _return = func(*args, **kwargs)
            with open(path, mode=mode) as fh:
                fh.write(_return)
            return _return
        return inner_decorator
    return outer_decorator


class Webpage(object):
    """
    A specified URL class, which can perform few utility functions for an webpage associated.
    """

    def __init__(self, url):
        self.url = url
        self._contents = None
        self.response = None

    @store_back_output(path="zdnet-security")
    def get_contents(self, **kwargs):
        """
        Makes the request to specified URL and get backs the contents.
        :return: HTML contents of the webpage. Throws Expection in case of failure in HTTP response.
        """
        try:
            self.response = requests.get(url=self.url, verify=False)
            if self.response.status_code == requests.codes.ALL_OK:
                self._contents = self.response.content.replace("><", ">\n<")
            else:
                self._contents = None
                raise requests.HTTPError("Got {0} page response".format(self.response.status_code))
        except Exception as e:
            raise e.__class__(e.message)
        return self._contents

    def get_patterns(self, pattern, string=None):
        """
        Takes in the Regular Expression Pattern to match with contents from Webpage or string specified.
        :param pattern: Regular expression string.
        :param string: Optional. String to match with RE.
        :return: All the found pattern in list. Throws Expection if not valid contents are found.
        """
        pattern = r'{0}'.format(pattern)
        if string is None:
            string = self.get_contents()
        elif not self._contents:
            raise ValueError("No valid contents found to parse")
        find_all = re.findall(pattern=pattern, string=string)
        return find_all

    def __repr__(self):
        return "<WebPage {0}>".format(self.url)