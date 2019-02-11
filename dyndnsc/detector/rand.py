# -*- coding: utf-8 -*-

"""Module containing logic for random IP based detectors."""

import logging
from random import randint

from .base import IPDetector, AF_INET
from ..common.six import ipaddress, ipnetwork

LOG = logging.getLogger(__name__)


def random_ip():
    """Return a randomly generated IPv4 address.

    :return: ip address
    """
    return ipaddress(
        "%i.%i.%i.%i" % (
            randint(1, 254), randint(1, 254), randint(1, 254), randint(1, 254)  # noqa: S311
        )
    )


class RandomIPGenerator(object):
    """The random IP generator."""

    def __init__(self, num=None):
        """Initialize."""
        self._max = num

        # Reserved list from http://www.iana.org/assignments/ipv4-address-space
        # (dated  2010-02-22)
        self._reserved_netmasks = frozenset([
            "0.0.0.0/8",
            "5.0.0.0/8",
            "10.0.0.0/8",
            "23.0.0.0/8",
            "31.0.0.0/8",
            "36.0.0.0/8",
            "39.0.0.0/8",
            "42.0.0.0/8",
            "127.0.0.0/8",
            "169.254.0.0/16",
            "172.16.0.0/12",
            "192.168.0.0/16",
            "224.0.0.0/3",
            "240.0.0.0/8"
        ])

    def is_reserved_ip(self, ip):
        """Check if the given ip address is in a reserved ipv4 address space.

        :param ip: ip address
        :return: boolean
        """
        theip = ipaddress(ip)
        for res in self._reserved_netmasks:
            if theip in ipnetwork(res):
                return True
        return False

    def random_public_ip(self):
        """Return a randomly generated, public IPv4 address.

        :return: ip address
        """
        randomip = random_ip()
        while self.is_reserved_ip(randomip):
            randomip = random_ip()
        return randomip

    def __iter__(self):
        """Iterate over this instance.."""
        count = 0
        while self._max is None or count < self._max:
            yield self.random_public_ip()
            count += 1


class IPDetector_Random(IPDetector):
    """Detect randomly generated IP addresses."""

    configuration_key = "random"

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super(IPDetector_Random, self).__init__(*args, **kwargs)

        self.opts_family = AF_INET
        self.rips = RandomIPGenerator()

    def can_detect_offline(self):
        """
        Detect the IP address.

        :return: True
        """
        return True

    def detect(self):
        """Detect IP and return it."""
        for theip in self.rips:
            LOG.debug("detected %s", str(theip))
            self.set_current_value(str(theip))
            return str(theip)
