# -*- coding: utf-8 -*-

"""Module containing logic for teredo based detectors."""

import logging

from .iface import IPDetector_Iface, AF_INET6

LOG = logging.getLogger(__name__)


class IPDetector_Teredo(IPDetector_Iface):
    """IPDetector to detect a Teredo ipv6 address of a local interface.

    Bits 0 to 31 of the ipv6 address are set to the Teredo prefix (normally
    2001:0000::/32).
    This detector only checks the first 16 bits!
    See http://en.wikipedia.org/wiki/Teredo_tunneling for more information on
    Teredo.

    Inherits IPDetector_Iface and sets default options only.
    """

    configuration_key = "teredo"

    def __init__(self, iface="tun0", netmask="2001:0000::/32", *args, **kwargs):
        """Initializer."""
        super(IPDetector_Teredo, self).__init__(*args, **kwargs)

        self.opts_iface = iface
        self.opts_netmask = netmask
        self.opts_family = AF_INET6
