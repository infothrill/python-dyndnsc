# -*- coding: utf-8 -*-

"""Module containing logic for socket based detectors."""

import logging

from .base import IPDetector, AF_INET6
from ..common.detect_ip import detect_ip, IPV4, IPV6_PUBLIC, GetIpException

LOG = logging.getLogger(__name__)


class IPDetector_Socket(IPDetector):
    """Detect IPs used by the system to communicate with outside world."""

    configuration_key = "socket"

    def __init__(self, family=None, *args, **kwargs):
        """
        Initializer.

        :param family: IP address family (default: INET, possible: INET6)
        """
        super(IPDetector_Socket, self).__init__(*args, family=family, **kwargs)

    def can_detect_offline(self):
        """Return False, this detector works offline."""
        # unsure about this. detector does not really transmit data to outside,
        # but unsure if it gives the wanted IPs if system is offline
        return False

    def detect(self):
        """Detect the IP address."""
        if self.opts_family == AF_INET6:
            kind = IPV6_PUBLIC
        else:  # 'INET':
            kind = IPV4
        theip = None
        try:
            theip = detect_ip(kind)
        except GetIpException:
            LOG.exception("socket detector raised an exception:")
        self.set_current_value(theip)
        return theip
