# -*- coding: utf-8 -*-

"""Module containing logic for dns based detectors."""

import socket
import logging

from .base import IPDetector, AF_INET, AF_INET6, AF_UNSPEC

LOG = logging.getLogger(__name__)


def resolve(hostname, family=AF_UNSPEC):
    """
    Resolve hostname to one or more IP addresses through the operating system.

    Resolution is carried out for the given address family. If no
    address family is specified, only IPv4 and IPv6 addresses are returned. If
    multiple IP addresses are found, all are returned.

    :param family: AF_INET or AF_INET6 or AF_UNSPEC (default)
    :return: tuple of unique IP addresses
    """
    af_ok = (AF_INET, AF_INET6)
    if family != AF_UNSPEC and family not in af_ok:
        raise ValueError("Invalid family '%s'" % family)
    ips = ()
    try:
        addrinfo = socket.getaddrinfo(hostname, None, family)
    except socket.gaierror as exc:
        # EAI_NODATA and EAI_NONAME are expected if this name is not (yet)
        # present in DNS
        if exc.errno not in (socket.EAI_NODATA, socket.EAI_NONAME):
            LOG.debug("socket.getaddrinfo() raised an exception", exc_info=exc)
    else:
        if family == AF_UNSPEC:
            ips = tuple({item[4][0] for item in addrinfo if item[0] in af_ok})
        else:
            ips = tuple({item[4][0] for item in addrinfo})
    return ips


class IPDetector_DNS(IPDetector):
    """Class to resolve a hostname using socket.getaddrinfo()."""

    configuration_key = "dns"

    def __init__(self, hostname=None, family=None, *args, **kwargs):
        """
        Initializer.

        :param hostname: host name to query from DNS
        :param family: IP address family (default: '' (ANY), also possible: 'INET', 'INET6')
        """
        super(IPDetector_DNS, self).__init__(*args, family=family, **kwargs)

        self.opts_hostname = hostname

        if self.opts_hostname is None:
            raise ValueError(
                "IPDetector_DNS(): a hostname to be queried in DNS must be specified!")

    def can_detect_offline(self):
        """Return false, as this detector generates dns traffic.

        :return: False
        """
        return False

    def detect(self):
        """
        Resolve the hostname to an IP address through the operating system.

        Depending on the 'family' option, either ipv4 or ipv6 resolution is
        carried out.

        If multiple IP addresses are found, the first one is returned.

        :return: ip address
        """
        theip = next(iter(resolve(self.opts_hostname, self.opts_family)), None)
        self.set_current_value(theip)
        return theip
