# -*- coding: utf-8 -*-

import unittest
import logging

import dyndnsc

logging.basicConfig(level=logging.DEBUG)


class PluginDetectorTests(unittest.TestCase):
    def test_detector_builtin(self):
        import dyndnsc.detector.builtin
        self.assertTrue(len(dyndnsc.detector.builtin.plugins) > 0)

    def test_zdetector_interfaces(self):
        import dyndnsc.detector.manager
        self.assertTrue(len(dyndnsc.detector.manager.detector_classes()) > 0)
        for cls in dyndnsc.detector.manager.detector_classes():
            self.assertTrue(hasattr(cls, 'getName'))
        self.assertRaises(KeyError, dyndnsc.detector.manager.get_detector_class, 'nonexistant')


class IndividualDetectorTests(unittest.TestCase):
    def test_dns_detector(self):
        import dyndnsc.detector.dns
        NAME = "dns"
        self.assertEqual(NAME, dyndnsc.detector.dns.IPDetector_DNS.getName())
        detector = dyndnsc.detector.dns.IPDetector_DNS("localhost")
        self.assertFalse(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1"))
        self.assertTrue(detector.getCurrentValue() in ("::1", "127.0.0.1"))

    def test_command_detector(self):
        import dyndnsc.detector.command
        NAME = "command"
        cmd = "echo 127.0.0.1"
        self.assertEqual(NAME, dyndnsc.detector.command.IPDetector_Command.getName())
        detector = dyndnsc.detector.command.IPDetector_Command({"command": cmd})
        self.assertFalse(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1"))
        self.assertTrue(detector.getCurrentValue() in ("::1", "127.0.0.1"))

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
        NAME = "random"
        self.assertEqual(NAME, dyndnsc.detector.rand.IPDetector_Random.getName())
        detector = dyndnsc.detector.rand.IPDetector_Random()
        self.assertTrue(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (str,))

    def test_iface_detector(self):
        import dyndnsc.detector.iface
        NAME = "iface"
        self.assertEqual(NAME, dyndnsc.detector.iface.IPDetector_Iface.getName())
        detector = dyndnsc.detector.iface.IPDetector_Iface()
        self.assertTrue(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))

    def test_teredo_detector(self):
        import dyndnsc.detector.teredo
        NAME = "teredo"
        self.assertEqual(NAME, dyndnsc.detector.teredo.IPDetector_Teredo.getName())
        detector = dyndnsc.detector.teredo.IPDetector_Teredo()
        self.assertTrue(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))

        detector = dyndnsc.detector.teredo.IPDetector_Teredo(options={'iface': 'foo0'})
        self.assertEqual(None, detector.detect())

    def test_webcheck_parsers(self):
        import dyndnsc.detector.webcheck
        self.assertEqual(None, dyndnsc.detector.webcheck._parser_checkip(""))
        self.assertEqual("127.0.0.1", dyndnsc.detector.webcheck._parser_checkip("Current IP Address: 127.0.0.1"))

        self.assertEqual(None, dyndnsc.detector.webcheck._parser_plain(""))
        self.assertEqual("127.0.0.1", dyndnsc.detector.webcheck._parser_plain("127.0.0.1"))

        self.assertEqual(None, dyndnsc.detector.webcheck._parser_freedns_afraid(""))
        self.assertEqual("127.0.0.1", dyndnsc.detector.webcheck._parser_freedns_afraid("Detected IP : 127.0.0.1"))

    def test_webcheck(self):
        import dyndnsc.detector.webcheck
        NAME = "webcheck"
        self.assertEqual(NAME, dyndnsc.detector.webcheck.IPDetector_WebCheck.getName())
        detector = dyndnsc.detector.webcheck.IPDetector_WebCheck()
        self.assertFalse(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
