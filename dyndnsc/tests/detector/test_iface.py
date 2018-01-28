# -*- coding: utf-8 -*-

"""Tests for the iface detector."""


import unittest

from dyndnsc.detector.base import AF_INET6
from dyndnsc.common.six import string_types


def give_me_an_interface_ipv6():
    """Return a local ipv6 interface or None."""
    import netifaces
    for interface in netifaces.interfaces():
        if netifaces.AF_INET6 in netifaces.ifaddresses(interface):
            return interface
    return None


def give_me_an_interface_ipv4():
    """Return a local ipv4 interface or None."""
    import netifaces
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            return interface
    return None


class IfaceDetectorTest(unittest.TestCase):
    """Test cases for iface detector."""

    def test_iface_detector(self):
        """Run iface tests."""
        from dyndnsc.detector import iface
        self.assertEqual("iface", iface.IPDetector_Iface.configuration_key)
        # auto-detect an interface:
        interface = give_me_an_interface_ipv4()
        self.assertNotEqual(None, interface)
        detector = iface.IPDetector_Iface(iface=interface)
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), string_types + (type(None),)))
        # empty interface name must not fail construction
        self.assertIsInstance(iface.IPDetector_Iface(iface=None), iface.IPDetector_Iface)
        # invalid netmask must fail construction
        self.assertRaises(ValueError, iface.IPDetector_Iface, netmask="fubar")
        # unknown address family  must fail construction
        self.assertRaises(ValueError, iface.IPDetector_Iface, family="bla")

    def test_teredo_detector(self):
        """Run teredo tests."""
        from dyndnsc.detector import teredo
        self.assertEqual("teredo", teredo.IPDetector_Teredo.configuration_key)
        # auto-detect an interface:
        interface = give_me_an_interface_ipv6()
        if interface is not None:  # we have ip6 support
            detector = teredo.IPDetector_Teredo(iface=interface)
            self.assertTrue(detector.can_detect_offline())
            self.assertEqual(AF_INET6, detector.af())
            self.assertEqual(None, detector.get_current_value())
            self.assertTrue(isinstance(detector.detect(), string_types + (type(None),)))
            # self.assertNotEqual(None, detector.netmask)

        detector = teredo.IPDetector_Teredo(iface="foo0")
        self.assertEqual(None, detector.detect())
