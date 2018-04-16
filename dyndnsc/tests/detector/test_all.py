# -*- coding: utf-8 -*-

"""Tests for detectors."""


import unittest

from dyndnsc.detector.base import AF_INET, AF_INET6, AF_UNSPEC

HAVE_IPV6 = True
try:
    import socket
    socket.socket(socket.AF_INET6, socket.SOCK_DGRAM).connect(("ipv6.google.com", 0))
except (OSError, socket.error, socket.gaierror):
    HAVE_IPV6 = False


class TestPluginDetectors(unittest.TestCase):
    """Test cases for detector discovery and management."""

    def test_detector_builtin(self):
        """Test that we have at least one builtin detector class."""
        import dyndnsc.detector.builtin
        self.assertTrue(len(dyndnsc.detector.builtin.PLUGINS) > 0)

    def test_detector_interfaces(self):
        """Test that each builtin detector class has certain apis."""
        import dyndnsc.detector.manager
        self.assertTrue(len(dyndnsc.detector.manager.detector_classes()) > 0)
        for cls in dyndnsc.detector.manager.detector_classes():
            self.assertTrue(hasattr(cls, "configuration_key"))
            self.assertTrue(hasattr(cls, "af"))
        self.assertRaises(ValueError, dyndnsc.detector.manager.get_detector_class, "nonexistent")


class TestIndividualDetectors(unittest.TestCase):
    """Test cases for detectors."""

    def test_dns_resolve(self):
        """Run tests for DNS resolution."""
        import dyndnsc.detector.dns as ns
        self.assertTrue(len(ns.resolve("localhost")) > 0)
        self.assertTrue(len(ns.resolve("localhost", family=ns.AF_INET)) > 0)

    def test_detector_state_changes(self):
        """Run tests for IPDetector state changes."""
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
        """Run tests for IPDetector_DNS."""
        import dyndnsc.detector.dns as ns
        self.assertEqual("dns", ns.IPDetector_DNS.configuration_key)
        detector = ns.IPDetector_DNS(hostname="localhost")
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_UNSPEC, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), str)))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1", "fe80::1%lo0"))
        self.assertTrue(detector.get_current_value() in ("::1", "127.0.0.1", "fe80::1%lo0"))
        # test address family restriction to ipv4:
        detector = ns.IPDetector_DNS(hostname="localhost", family="INET")
        self.assertEqual(AF_INET, detector.af())
        self.assertTrue(detector.detect() in ("127.0.0.1", ))
        # test address family restriction to ipv6:
        if HAVE_IPV6:
            detector = ns.IPDetector_DNS(hostname="localhost", family="INET6")
            self.assertEqual(AF_INET6, detector.af())
            val = detector.detect()
            self.assertTrue(val in ("::1", "fe80::1%lo0"), "%r not known" % val)

    def test_command_detector(self):
        """Run tests for IPDetector_Command."""
        import dyndnsc.detector.command
        cmd = "echo 127.0.0.1"
        self.assertEqual("command", dyndnsc.detector.command.IPDetector_Command.configuration_key)
        detector = dyndnsc.detector.command.IPDetector_Command(command=cmd)
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_UNSPEC, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), str)))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1"))
        self.assertTrue(detector.get_current_value() in ("::1", "127.0.0.1"))

        # test address family restriction to ipv4:
        detector = dyndnsc.detector.command.IPDetector_Command(command=cmd, family="INET")
        self.assertEqual(AF_INET, detector.af())

        # test address family restriction to ipv6:
        detector = dyndnsc.detector.command.IPDetector_Command(command=cmd, family="INET6")
        self.assertEqual(AF_INET6, detector.af())

    def test_rand_ip_generator(self):
        """Run tests for RandomIPGenerator."""
        import dyndnsc.detector.rand
        generator = dyndnsc.detector.rand.RandomIPGenerator()
        self.assertTrue(generator.is_reserved_ip("127.0.0.1"))
        self.assertFalse(generator.is_reserved_ip("83.169.1.157"))
        self.assertFalse(generator.is_reserved_ip(generator.random_public_ip()))
        # for the sake of randomness, detect a bunch of IPs:
        _count = 0
        generator = dyndnsc.detector.rand.RandomIPGenerator(100)
        for _count, theip in enumerate(generator):
            self.assertFalse(generator.is_reserved_ip(theip))
        self.assertEqual(_count, 99)

    def test_rand_detector(self):
        """Run tests for IPDetector_Random."""
        import dyndnsc.detector.rand
        self.assertEqual("random", dyndnsc.detector.rand.IPDetector_Random.configuration_key)
        detector = dyndnsc.detector.rand.IPDetector_Random()
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(AF_INET, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), str)))

    def test_socket_detector(self):
        """Run tests for IPDetector_Socket."""
        from dyndnsc.detector import socket_ip
        self.assertEqual("socket", socket_ip.IPDetector_Socket.configuration_key)
        detector = socket_ip.IPDetector_Socket(family="INET")
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_INET, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), str)))
        # unknown address family  must fail construction
        self.assertRaises(ValueError, socket_ip.IPDetector_Socket, family="bla")

    def test_webcheck_parsers(self):
        """Run tests for different webcheck parsers."""
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
        from dyndnsc.detector import webcheck
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
        """Run tests for IPDetectorWebCheck."""
        from dyndnsc.detector import webcheck
        self.assertEqual("webcheck4", webcheck.IPDetectorWebCheck.configuration_key)
        detector = webcheck.IPDetectorWebCheck()
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_INET, detector.af())
        self.assertEqual(None, detector.get_current_value())
        value = detector.detect()
        self.assertTrue(isinstance(value, (type(None), str)))

    def test_webcheck6(self):
        """Run tests for IPDetectorWebCheck6."""
        from dyndnsc.detector import webcheck
        self.assertEqual("webcheck6", webcheck.IPDetectorWebCheck6.configuration_key)
        detector = webcheck.IPDetectorWebCheck6()
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_INET6, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), str)))

    def test_webcheck46(self):
        """Run tests for IPDetectorWebCheck46."""
        from dyndnsc.detector import webcheck
        self.assertEqual("webcheck46", webcheck.IPDetectorWebCheck46.configuration_key)
        detector = webcheck.IPDetectorWebCheck46()
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(AF_UNSPEC, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), str)))

    def test_null(self):
        """Run tests for IPDetector_Null."""
        from dyndnsc.detector import null
        self.assertEqual("null", null.IPDetector_Null.configuration_key)
        detector = null.IPDetector_Null()
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(AF_UNSPEC, detector.af())
        self.assertEqual(None, detector.get_current_value())
        self.assertTrue(isinstance(detector.detect(), (type(None), str)))
