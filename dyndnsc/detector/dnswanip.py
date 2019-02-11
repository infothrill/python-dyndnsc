# -*- coding: utf-8 -*-

"""Module containing logic for DNS WAN IP detection.

See also https://www.cyberciti.biz/faq/how-to-find-my-public-ip-address-from-command-line-on-a-linux/
"""
from __future__ import absolute_import

import logging

import dns.resolver

from .base import IPDetector, AF_INET, AF_INET6
from .dns import resolve

LOG = logging.getLogger(__name__)


def find_ip(family=AF_INET, flavour="opendns"):
    """Find the publicly visible IP address of the current system.

    This uses public DNS infrastructure that implement a special DNS "hack" to
    return the IP address of the requester rather than some other address.

    :param family: address family, optional, default AF_INET (ipv4)
    :param flavour: selector for public infrastructure provider, optional
    """
    flavours = {
        "opendns": {
            AF_INET: {
                "@": ("resolver1.opendns.com", "resolver2.opendns.com"),
                "qname": "myip.opendns.com",
                "rdtype": "A",
            },
            AF_INET6: {
                "@": ("resolver1.ipv6-sandbox.opendns.com", "resolver2.ipv6-sandbox.opendns.com"),
                "qname": "myip.opendns.com",
                "rdtype": "AAAA",
            },
        },
    }

    flavour = flavours["opendns"]
    resolver = dns.resolver.Resolver()
    # specify the custom nameservers to be used (as IPs):
    resolver.nameservers = [next(iter(resolve(h, family=family))) for h in flavour[family]["@"]]

    answers = resolver.query(qname=flavour[family]["qname"], rdtype=flavour[family]["rdtype"])
    for rdata in answers:
        return rdata.address
    return None


class IPDetector_DnsWanIp(IPDetector):
    """Detect the internet visible IP address using publicly available DNS infrastructure."""

    configuration_key = "dnswanip"

    def __init__(self, family=None, *args, **kwargs):
        """
        Initializer.

        :param family: IP address family (default: '' (ANY), also possible: 'INET', 'INET6')
        """
        if family is None:
            family = AF_INET
        super(IPDetector_DnsWanIp, self).__init__(*args, family=family, **kwargs)

    def can_detect_offline(self):
        """Return false, as this detector generates dns traffic.

        :return: False
        """
        return False

    def detect(self):
        """
        Detect the WAN IP of the current process through DNS.

        Depending on the 'family' option, either ipv4 or ipv6 resolution is
        carried out.

        :return: ip address
        """
        theip = find_ip(family=self.opts_family)
        self.set_current_value(theip)
        return theip
