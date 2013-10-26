# -*- coding: utf-8 -*-

import logging
import re

import IPy
import requests

from .base import IPDetector

log = logging.getLogger(__name__)


class IPDetector_WebCheck(IPDetector):
    """Class to detect an IP address as seen by an online web site that returns parsable output"""

    @staticmethod
    def getName():
        return "webcheck"

    def canDetectOffline(self):
        """Returns false, as this detector generates http traffic"""
        return False

    def _getClientIPFromUrl(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                regex = re.compile("Current IP Address: (.*?)(<.*){0,1}$")
                for line in r.text.splitlines():
                    matchObj = regex.search(line)
                    if not matchObj is None:
                        return str(IPy.IP(matchObj.group(1)))
        except (requests.exceptions.RequestException):
            pass
        return None

    def detect(self):
        # self.LOG("detect WebCheck")
        from random import choice
        urls = (
                "http://checkip.dyndns.org/",
                "http://checkip.eurodyndns.org/",
                "http://dynamic.zoneedit.com/checkip.html",  # renders bad stuff if queried too quickly, but that's fine ;-)
                "http://ipcheck.rehbein.net/"
                "http://www.antifart.com/stuff/checkip/",
                )
        theip = self._getClientIPFromUrl(choice(urls))
        if theip is None:
            log.info("Could not detect IP using webchecking! Offline?")
        self.setCurrentValue(theip)
        return theip
