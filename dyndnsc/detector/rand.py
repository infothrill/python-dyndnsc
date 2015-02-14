# -*- coding: utf-8 -*-

import logging
import random

from .base import IPDetector, AF_INET
from ..common.six import ipaddress, ipnetwork

log = logging.getLogger(__name__)


class RandomIPGenerator(object):
    def __init__(self, maxRandomTries=None):
        self.maxRandomTries = maxRandomTries

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

    def isReservedIP(self, ip):
        """Check if the given ip address is in a reserved ipv4 address space.

        :param ip: ip address
        :return: boolean
        """
        theip = ipaddress(ip)
        for res in self._reserved_netmasks:
            if theip in ipnetwork(res):
                return True
        return False

    def randomIP(self):
        """Return a randomly generated IPv4 address that is not in a reserved
        ipv4 address space

        :return: ip address
        """
        randomip = ipaddress("%i.%i.%i.%i" % (random.randint(1, 254),
                                              random.randint(1, 254),
                                              random.randint(1, 254),
                                              random.randint(1, 254)))
        while self.isReservedIP(randomip):
            randomip = ipaddress("%i.%i.%i.%i" % (random.randint(1, 254),
                                                  random.randint(1, 254),
                                                  random.randint(1, 254),
                                                  random.randint(1, 254)))
        return randomip

    def next(self):
        return self.__next__()

    def __next__(self):
        """Generator that returns randomly generated IPv4 addresses that are
        not in a reserved ipv4 address space until we hit self.maxRandomTries

        :return: ip address
        """
        if self.maxRandomTries is None or self.maxRandomTries > 0:
            generate = True
        else:
            generate = False
        c = 0
        while generate:
            if self.maxRandomTries is not None:
                c += 1
            yield self.randomIP()
            if self.maxRandomTries is not None and c < self.maxRandomTries:
                generate = False

        raise StopIteration

    def __iter__(self):
        """Iterator for this class. See method next()."""
        return next(self)


class IPDetector_Random(IPDetector):
    """For testing: detect randomly generated IP addresses."""
    def __init__(self, *args, **kwargs):
        super(IPDetector_Random, self).__init__(*args, **kwargs)

        self.opts_family = AF_INET
        self.rips = RandomIPGenerator()

    @staticmethod
    def names():
        return ("random",)

    def can_detect_offline(self):
        """:return: True"""
        return True

    def detect(self):
        for theip in self.rips:
            log.debug('detected %s', str(theip))
            self.set_current_value(str(theip))
            return str(theip)
