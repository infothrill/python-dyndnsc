# -*- coding: utf-8 -*-

import socket

from .base import IPDetector


class IPDetector_DNS(IPDetector):
    """Class to resolve a hostname using socket.getaddrinfo()"""
    def __init__(self, hostname):
        self._hostname = hostname
        super(IPDetector_DNS, self).__init__()

    @staticmethod
    def getName():
        return "dns"

    def canDetectOffline(self):
        """Returns false, as this detector generates dns traffic"""
        return False

    def detect(self):
        try:
            theip = socket.getaddrinfo(self._hostname, None)[0][4][0]
        except:
            # logging.debug("WARN: dns is None")
            theip = None
        # logging.debug("dnsdetect for %s: %s", self.hostname, ip)
        self.setCurrentValue(theip)
        return theip
