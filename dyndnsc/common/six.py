# -*- coding: utf-8 -*-

"""Module for providing python compatibility across interpreter versions."""

import sys

if sys.version_info < (3, 0):
    from cStringIO import StringIO
else:
    from io import StringIO

if sys.version_info < (3, 3):
    import IPy as _IPy

    def ipaddress(addr):
        return _IPy.IP(addr)

    def ipnetwork(addr):
        return _IPy.IP(addr)

else:
    import ipaddress as _ipaddress

    def ipaddress(addr):
        return _ipaddress.ip_address(addr)

    def ipnetwork(addr):
        return _ipaddress.ip_network(addr)
