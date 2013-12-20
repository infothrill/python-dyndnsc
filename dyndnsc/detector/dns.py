# -*- coding: utf-8 -*-

import socket
import logging

from .base import IPDetector

log = logging.getLogger(__name__)

# expose these constants for users of this module:
AF_INET = socket.AF_INET
AF_INET6 = socket.AF_INET6


def resolve(hostname, family=None):
    '''
    Resolves the hostname to one or more IP addresses through the operating
    system. Resolution is carried out for the given address family. If no
    address family is specified, only IPv4 and IPv6 addresses are returned. If
    multiple IP addresses are found, all are returned.

    :return: tuple of unique IP addresses
    '''
    af_ok = (AF_INET, AF_INET6)
    if family is not None and family not in af_ok:
        raise ValueError("Invalid AF_ '%s'" % family)
    ips = ()
    try:
        if family is None:
            addrinfo = socket.getaddrinfo(hostname, None)
        else:
            addrinfo = socket.getaddrinfo(hostname, None, family)
    except socket.gaierror as exc:
        log.debug("socket.getaddrinfo() raised an exception", exc_info=exc)
    else:
        if family is None:
            ips = tuple(set(
                        [item[4][0] for item in addrinfo if item[0] in af_ok]
                        ))
        else:
            ips = tuple(set([item[4][0] for item in addrinfo]))
    return ips


class IPDetector_DNS(IPDetector):
    """Class to resolve a hostname using socket.getaddrinfo()"""
    def __init__(self, hostname):
        self._hostname = hostname
        super(IPDetector_DNS, self).__init__()

    @staticmethod
    def names():
        return ("dns",)

    def can_detect_offline(self):
        """Returns false, as this detector generates dns traffic

        :return: False
        """
        return False

    def detect(self):
        '''
        Resolves the hostname to an IP address through the operating system.
        Both ipv4 and ipv6 resolution is carried out. If multiple IP addresses
        are found, the first one is returned.

        :return: ip address
        '''
        ips = resolve(self._hostname)
        if len(ips) > 0:
            theip = ips[0]
        else:
            theip = None
        self.set_current_value(theip)
        return theip
