# -*- coding: utf-8 -*-

import logging

from .iface import IPDetector_Iface

log = logging.getLogger(__name__)


class IPDetector_Teredo(IPDetector_Iface):
    """IPDetector to detect a Teredo ipv6 address of a local interface.
    Bits 0 to 31 of the ipv6 address are set to the Teredo prefix (normally
    2001:0000::/32).
    This detector only checks the first 16 bits!
    See http://en.wikipedia.org/wiki/Teredo_tunneling for more information on
    Teredo.

    Inherits IPDetector_Iface and sets default options only
    """
    def __init__(self, *args, **kwargs):
        """
        Initializer
        """
        self.opts_iface = kwargs.get('iface', 'tun0')
        self.opts_family = kwargs.get('family', 'INET6')
        self.opts_netmask = kwargs.get('netmask', '2001:0000::/32')
        super(IPDetector_Teredo, self).__init__(**kwargs)

    @staticmethod
    def names():
        return ("teredo",)
