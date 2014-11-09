# -*- coding: utf-8 -*-

import logging

from .base import IPDetector
from ..common.detect_ip import detect_ip, IPV4, IPV6_PUBLIC, GetIpException

log = logging.getLogger(__name__)


class IPDetector_Socket(IPDetector):
    """
    IPDetector to detect IPs used by the system to communicate with outside world.
    """
    def __init__(self, options=None):
        """
        Constructor
        @param options: dictionary

        available options:

        family: IP address family (default: INET, possible: INET6)
        """
        if options is None:
            options = {}
        # default options:
        self.opts = {
            'family': 'INET',
        }
        for k in options.keys():
            log.debug("%s explicitly got option: %s -> %s",
                      self.__class__.__name__, k, options[k])
            self.opts[k] = options[k]

        # ensure address family is understood:
        if self.opts['family'] not in ('INET', 'INET6'):
            raise ValueError("Unsupported address family '%s' specified!" %
                             self.opts['family'])

        super(IPDetector_Socket, self).__init__()

    @staticmethod
    def names():
        return ("socket",)

    def can_detect_offline(self):
        # unsure about this. detector does not really transmit data to outside,
        # but unsure if it gives the wanted IPs if system is offline
        return False

    def detect(self):
        if self.opts['family'] == 'INET6':
            kind = IPV6_PUBLIC
        else:  # 'INET':
            kind = IPV4
        theip = None
        try:
            theip = detect_ip(kind)
        except GetIpException:
            log.exception("socket detector raised an exception:")
        self.set_current_value(theip)
        return theip
