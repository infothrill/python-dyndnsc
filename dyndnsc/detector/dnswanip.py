# -*- coding: utf-8 -*-

"""Module containing logic for DNS WAN IP detection.

See also https://www.cyberciti.biz/faq/how-to-find-my-public-ip-address-from-command-line-on-a-linux/
"""
from __future__ import absolute_import

import logging

import dns.resolver

from .base import IPDetector, AF_INET, AF_INET6

LOG = logging.getLogger(__name__)


def find_ip(family=AF_INET, provider="opendns"):
    """Find the publicly visible IP address of the current system.

    This uses public DNS infrastructure that implement a special DNS "hack" to
    return the IP address of the requester rather than some other address.

    :param family: address family, optional, default AF_INET (ipv4)
    :param flavour: selector for public infrastructure provider, optional
    """
    dnswanipproviders = {
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

    dnswanipprovider = dnswanipproviders[provider]  # only option as of now

    resolver = dns.resolver.Resolver()
    # first, get the IPs of the DNS servers:
    nameservers = []
    for dnsservername in dnswanipprovider[family]["@"]:
        _answers = resolver.query(qname=dnsservername, rdtype=dnswanipprovider[family]["rdtype"])
        nameservers.extend([rdata.address for rdata in _answers])
    # specify the nameservers to be used:
    resolver.nameservers = nameservers
    # finally, attempt to discover our WAN IP by querying the DNS:
    answers = resolver.query(qname=dnswanipprovider[family]["qname"], rdtype=dnswanipprovider[family]["rdtype"])
    for rdata in answers:
        return rdata.address
    return None


class IPDetector_DnsWanIp(IPDetector):
    """Detect the internet visible IP address using publicly available DNS infrastructure."""

    configuration_key = "dnswanip"

    def __init__(self, family=None, *args, **kwargs):
        """
        Initialize.

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
