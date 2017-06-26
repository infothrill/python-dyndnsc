# -*- coding: utf-8 -*-

import sys
import unittest
import logging

from dyndnsc.detector.base import AF_INET6

# more py23 madness
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_type = str
else:
    string_type = basestring


def is_netifaces_available():
    try:
        import netifaces
    except ImportError:
        return False
    else:
        return True


def give_me_an_interface_ipv6():
    import netifaces
    for interface in netifaces.interfaces():
        if netifaces.AF_INET6 in netifaces.ifaddresses(interface):
            return interface
    return None


def give_me_an_interface_ipv4():
    import netifaces
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            return interface
    return None


class IfaceDetectorTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_iface_detector(self):
        # py3: can user unittest.skipIf(condition, reason)
        if not is_netifaces_available():
            return
        import dyndnsc.detector.iface as iface
        self.assertTrue("iface" in iface.IPDetector_Iface.names())
        # auto-detect an interface:
        interface = give_me_an_interface_ipv4()
        self.assertNotEqual(None, interface)
        detector = iface.IPDetector_Iface(iface=interface)
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), string_type)))
        # empty interface name must not fail construction
        # broken in python2.6
        # self.assertIsInstance(iface.IPDetector_Iface(iface=None), iface.IPDetector_Iface)
        self.assertEqual(type(iface.IPDetector_Iface(iface=None)), iface.IPDetector_Iface)
        # invalid netmask must fail construction
        self.assertRaises(ValueError, iface.IPDetector_Iface, netmask='fubar')
        # unknown address family  must fail construction
        self.assertRaises(ValueError, iface.IPDetector_Iface, family='bla')

    def test_teredo_detector(self):
        # py3: can user unittest.skipIf(condition, reason)
        if not is_netifaces_available():
            return
        import dyndnsc.detector.teredo as teredo
        self.assertTrue("teredo" in teredo.IPDetector_Teredo.names())
        # auto-detect an interface:
        interface = give_me_an_interface_ipv6()
        if interface is not None:  # we have ip6 support
            detector = teredo.IPDetector_Teredo(iface=interface)
            self.assertTrue(detector.can_detect_offline())
            self.assertEqual(AF_INET6, detector.af())
            self.assertEqual(None, detector.get_current_value())
            self.assertTrue(isinstance(detector.detect(), (type(None), string_type)))
            # self.assertNotEqual(None, detector.netmask)

        detector = teredo.IPDetector_Teredo(iface='foo0')
        self.assertEqual(None, detector.detect())
