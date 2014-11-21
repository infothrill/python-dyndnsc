# -*- coding: utf-8 -*-

import socket
import logging

from .base import IPDetector

log = logging.getLogger(__name__)

# expose these constants for users of this module:
AF_UNSPEC = socket.AF_UNSPEC
AF_INET = socket.AF_INET
AF_INET6 = socket.AF_INET6


def resolve(hostname, family=AF_UNSPEC):
    '''
    Resolves the hostname to one or more IP addresses through the operating
    system. Resolution is carried out for the given address family. If no
    address family is specified, only IPv4 and IPv6 addresses are returned. If
    multiple IP addresses are found, all are returned.

    :param family: AF_INET or AF_INET6 or 0 (ANY, default)
    :return: tuple of unique IP addresses
    '''
    af_ok = (AF_INET, AF_INET6)
    if family != AF_UNSPEC and family not in af_ok:
        raise ValueError("Invalid family '%s'" % family)
    ips = ()
    try:
        addrinfo = socket.getaddrinfo(hostname, None, family)
    except socket.gaierror as exc:
        # EAI_NODATA and EAI_NONAME are expected if this name is not (yet) present in DNS
        if exc.errno not in (socket.EAI_NODATA, socket.EAI_NONAME):
            log.debug("socket.getaddrinfo() raised an exception", exc_info=exc)
    else:
        if family == AF_UNSPEC:
            ips = tuple(set(
                        [item[4][0] for item in addrinfo if item[0] in af_ok]
                        ))
        else:
            ips = tuple(set([item[4][0] for item in addrinfo]))
    return ips


class IPDetector_DNS(IPDetector):
    """Class to resolve a hostname using socket.getaddrinfo()"""

    def __init__(self, options=None, hostname_default=None):
        """
        Constructor
        @param options: dictionary
        @param hostname_default: a default hostname to use (if not given in options)

        available options:

        hostname: host name to query from DNS
        family: IP address family (default: '' (ANY), also possible: 'INET', 'INET6')
        """
        if options is None:
            options = {}
        # default options:
        self.opts = {
            'hostname': hostname_default,
            'family': "",
        }
        for k in options.keys():
            log.debug("%s explicitly got option: %s -> %s",
                      self.__class__.__name__, k, options[k])
            self.opts[k] = options[k]

        # ensure a hostname is given:
        if not self.opts['hostname']:
            raise ValueError("You need to give a hostname to query from DNS!")

        # ensure address family is understood:
        if self.opts['family'] not in ('', 'INET', 'INET6'):
            raise ValueError("Unsupported address family '%s' specified!" %
                             self.opts['family'])

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
        if self.opts['family'] == 'INET6':
            family = AF_INET6
        elif self.opts['family'] == 'INET':
            family = AF_INET
        else:
            family = None
        ips = resolve(self.opts['hostname'], family)
        if len(ips) > 0:
            theip = ips[0]
        else:
            theip = None
        self.set_current_value(theip)
        return theip
