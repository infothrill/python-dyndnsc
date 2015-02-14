# -*- coding: utf-8 -*-

import unittest
import netifaces
import logging

from dyndnsc.detector.base import AF_INET, AF_INET6, AF_UNSPEC


def give_me_an_interface_ipv6():
    for interface in netifaces.interfaces():
        if netifaces.AF_INET6 in netifaces.ifaddresses(interface):
            return interface
    return None


def give_me_an_interface_ipv4():
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            return interface
    return None


class TestPluginDetectors(unittest.TestCase):
    def test_detector_builtin(self):
        import dyndnsc.detector.builtin
        self.assertTrue(len(dyndnsc.detector.builtin.plugins) > 0)

    def test_zdetector_interfaces(self):
        import dyndnsc.detector.manager
        self.assertTrue(len(dyndnsc.detector.manager.detector_classes()) > 0)
        for cls in dyndnsc.detector.manager.detector_classes():
            self.assertTrue(hasattr(cls, 'names'))
            self.assertTrue(hasattr(cls, 'af'))
        self.assertRaises(KeyError, dyndnsc.detector.manager.get_detector_class, 'nonexistent')


class TestIndividualDetectors(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_dns_resolve(self):
        import dyndnsc.detector.dns as ns
        self.assertTrue(len(ns.resolve("localhost")) > 0)
        self.assertTrue(len(ns.resolve("localhost", family=ns.AF_INET)) > 0)

    def test_detector_base_state_changes(self):
        import dyndnsc.detector.base
        ip1 = "127.0.0.1"
        ip2 = "127.0.0.2"
        detector = dyndnsc.detector.base.IPDetector()

        self.assertEqual(None, detector.get_current_value())
        self.assertEqual(None, detector.get_old_value())
        self.assertFalse(detector.has_changed())

        # set to ip1
        self.assertEqual(ip1, detector.set_current_value(ip1))
        self.assertTrue(detector.has_changed())
        self.assertEqual(ip1, detector.get_current_value())
        self.assertEqual(None, detector.get_old_value())

        # set to ip2
        self.assertEqual(ip2, detector.set_current_value(ip2))
        self.assertEqual(ip2, detector.get_current_value())
        self.assertEqual(ip1, detector.get_old_value())
        self.assertTrue(detector.has_changed())

        # set again to ip2
        self.assertEqual(ip2, detector.set_current_value(ip2))
        self.assertFalse(detector.has_changed())
        self.assertEqual(ip2, detector.get_current_value())
        self.assertEqual(ip2, detector.get_old_value())

    def test_dns_detector(self):
        import dyndnsc.detector.dns as ns
        self.assertTrue("dns" in ns.IPDetector_DNS.names())
        detector = ns.IPDetector_DNS(hostname_default="localhost")
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_UNSPEC, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1", "fe80::1%lo0"))
        self.assertTrue(detector.get_current_value() in ("::1", "127.0.0.1", "fe80::1%lo0"))
        # test address family restriction to ipv4:
        detector = ns.IPDetector_DNS(hostname_default="localhost", family='INET')
        self.assertEqual(AF_INET, detector.af())
        self.assertTrue(detector.detect() in ("127.0.0.1", ))
        # test address family restriction to ipv6:
        detector = ns.IPDetector_DNS(hostname_default="localhost", family='INET6')
        self.assertEqual(AF_INET6, detector.af())
        self.assertTrue(detector.detect() in ("::1", "fe80::1%lo0"))

    def test_command_detector(self):
        import dyndnsc.detector.command
        cmd = "echo 127.0.0.1"
        self.assertTrue("command" in dyndnsc.detector.command.IPDetector_Command.names())
        detector = dyndnsc.detector.command.IPDetector_Command(command=cmd)
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_UNSPEC, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1"))
        self.assertTrue(detector.get_current_value() in ("::1", "127.0.0.1"))

        # test address family restriction to ipv4:
        detector = dyndnsc.detector.command.IPDetector_Command(command=cmd, family='INET')
        self.assertEqual(AF_INET, detector.af())

        # test address family restriction to ipv6:
        detector = dyndnsc.detector.command.IPDetector_Command(command=cmd, family='INET6')
        self.assertEqual(AF_INET6, detector.af())

    def test_rand_ip_generator(self):
        import dyndnsc.detector.rand
        generator = dyndnsc.detector.rand.RandomIPGenerator()
        self.assertTrue(generator.isReservedIP("127.0.0.1"))
        self.assertFalse(generator.isReservedIP("83.169.1.157"))
        self.assertFalse(generator.isReservedIP(generator.randomIP()))
        # for the sake of randomness, detect a bunch of IPs:
        MAX = 100
        generator = dyndnsc.detector.rand.RandomIPGenerator()
        for c, ip in enumerate(generator):
            self.assertFalse(generator.isReservedIP(ip))
            if c >= MAX:
                break

    def test_rand_detector(self):
        import dyndnsc.detector.rand
        self.assertTrue("random" in dyndnsc.detector.rand.IPDetector_Random.names())
        detector = dyndnsc.detector.rand.IPDetector_Random()
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(AF_INET, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (str,))

    def test_iface_detector(self):
        import dyndnsc.detector.iface as iface
        self.assertTrue("iface" in iface.IPDetector_Iface.names())
        # auto-detect an interface:
        interface = give_me_an_interface_ipv4()
        self.assertNotEqual(None, interface)
        detector = iface.IPDetector_Iface(iface=interface)
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        # empty interface name must not fail construction
        # broken in python2.6
        # self.assertIsInstance(iface.IPDetector_Iface(iface=None), iface.IPDetector_Iface)
        self.assertEqual(type(iface.IPDetector_Iface(iface=None)), iface.IPDetector_Iface)
        # invalid netmask must fail construction
        self.assertRaises(ValueError, iface.IPDetector_Iface, netmask='fubar')
        # unknown address family  must fail construction
        self.assertRaises(ValueError, iface.IPDetector_Iface, family='bla')

    def test_socket_detector(self):
        import dyndnsc.detector.socket_ip as socket_ip
        self.assertTrue("socket" in socket_ip.IPDetector_Socket.names())
        detector = socket_ip.IPDetector_Socket(family='INET')
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_INET, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        # unknown address family  must fail construction
        self.assertRaises(ValueError, socket_ip.IPDetector_Socket, family='bla')

    def test_teredo_detector(self):
        import dyndnsc.detector.teredo as teredo
        self.assertTrue("teredo" in teredo.IPDetector_Teredo.names())
        # auto-detect an interface:
        interface = give_me_an_interface_ipv6()
        self.assertNotEqual(None, interface)
        detector = teredo.IPDetector_Teredo(iface=interface)
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(AF_INET6, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        # self.assertNotEqual(None, detector.netmask)

        detector = teredo.IPDetector_Teredo(iface='foo0')
        self.assertEqual(None, detector.detect())

    def test_webcheck_parsers(self):
        test_data_checkip_dns_he_net = """<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
 <title>What is my IP address?</title>
</head>
<body>
Your IP address is : 127.0.0.1</body>
</html>
"""
        import dyndnsc.detector.webcheck as webcheck
        self.assertEqual(None, webcheck._parser_checkip(""))
        self.assertEqual("127.0.0.1", webcheck._parser_checkip("Current IP Address: 127.0.0.1"))

        self.assertEqual("127.0.0.1", webcheck._parser_checkip_dns_he_net(test_data_checkip_dns_he_net))

        self.assertEqual(None, webcheck._parser_plain(""))
        self.assertEqual("127.0.0.1", webcheck._parser_plain("127.0.0.1"))

        self.assertEqual(None, webcheck._parser_freedns_afraid(""))
        self.assertEqual("127.0.0.1", webcheck._parser_freedns_afraid("Detected IP : 127.0.0.1"))

        self.assertEqual(None, webcheck._parser_jsonip(""))
        self.assertEqual("127.0.0.1", webcheck._parser_jsonip(
            r'{"ip":"127.0.0.1","about":"/about","Pro!":"http://getjsonip.com"}'))

    def test_webcheck(self):
        import dyndnsc.detector.webcheck as webcheck
        self.assertTrue("webcheck" in webcheck.IPDetectorWebCheck.names())
        detector = webcheck.IPDetectorWebCheck()
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_INET, detector.af())
        self.assertEqual(None, detector.get_current_value())
        det_type = type(detector.detect())
        self.assertTrue(det_type in (type(None), str), "Type '%s' invalid" % str(det_type))

    def test_webcheck6(self):
        import dyndnsc.detector.webcheck as webcheck
        self.assertTrue("webcheck6" in webcheck.IPDetectorWebCheck6.names())
        detector = webcheck.IPDetectorWebCheck6()
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_INET6, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (type(None), str))

    def test_webcheck46(self):
        import dyndnsc.detector.webcheck as webcheck
        self.assertTrue("webcheck46" in webcheck.IPDetectorWebCheck46.names())
        detector = webcheck.IPDetectorWebCheck46()
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_UNSPEC, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(type(detector.detect()) in (type(None), str))
