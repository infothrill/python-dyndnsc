# -*- coding: utf-8 -*-

"""Tests for detectors."""


import unittest

import pytest

from dyndnsc.common.six import string_types
from dyndnsc.common.six import ipaddress
from dyndnsc.detector.base import AF_INET, AF_INET6
from dyndnsc.detector.dnswanip import IPDetector_DnsWanIp

HAVE_IPV6 = True
try:
    import socket
    socket.socket(socket.AF_INET6, socket.SOCK_DGRAM).connect(("ipv6.google.com", 0))
except (OSError, socket.error, socket.gaierror):
    HAVE_IPV6 = False


class TestIndividualDetectors(unittest.TestCase):
    """Test cases for detectors."""

    def test_dnswanip_detector_class(self):
        """Run basic tests for IPDetector_DnsWanIp."""
        self.assertEqual("dnswanip", IPDetector_DnsWanIp.configuration_key)
        detector = IPDetector_DnsWanIp()
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(None, detector.get_current_value())
        # default family should be ipv4:
        detector = IPDetector_DnsWanIp(family=None)
        self.assertEqual(AF_INET, detector.af())
        detector = IPDetector_DnsWanIp(family=AF_INET)
        self.assertEqual(AF_INET, detector.af())
        detector = IPDetector_DnsWanIp(family=AF_INET6)
        self.assertEqual(AF_INET6, detector.af())

    def test_dnswanip_detector_ipv4(self):
        """Run ipv4 tests for IPDetector_DnsWanIp."""
        detector = IPDetector_DnsWanIp(family=AF_INET)
        result = detector.detect()
        self.assertTrue(isinstance(result, (type(None),) + string_types), type(result))
        # ensure the result is in fact an IP address:
        self.assertNotEqual(ipaddress(result), None)
        self.assertEqual(detector.get_current_value(), result)

    @pytest.mark.skipif(not HAVE_IPV6, reason="requires ipv6 connectivity")
    def test_dnswanip_detector_ipv6(self):
        """Run ipv6 tests for IPDetector_DnsWanIp."""
        if HAVE_IPV6:  # allow running test in IDE without pytest support
            detector = IPDetector_DnsWanIp(family=AF_INET6)
            result = detector.detect()
            self.assertTrue(isinstance(result, (type(None),) + string_types), type(result))
            # ensure the result is in fact an IP address:
            self.assertNotEqual(ipaddress(result), None)
            self.assertEqual(detector.get_current_value(), result)
