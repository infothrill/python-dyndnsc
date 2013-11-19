# -*- coding: utf-8 -*-

import unittest


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
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1"))
        self.assertTrue(detector.getCurrentValue() in ("::1", "127.0.0.1"))

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

    def test_command_detector(self):
        import dyndnsc.detector.command
        NAME = "command"
        cmd = "echo 127.0.0.1"
        self.assertEqual(NAME, dyndnsc.detector.command.IPDetector_Command.getName())
        detector = dyndnsc.detector.command.IPDetector_Command({"command": cmd})
        self.assertFalse(detector.can_detect_offline())
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
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (str,))

    def test_iface_detector(self):
        import dyndnsc.detector.iface
        NAME = "iface"
        self.assertEqual(NAME, dyndnsc.detector.iface.IPDetector_Iface.getName())
        detector = dyndnsc.detector.iface.IPDetector_Iface()
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        # make sure an invalid netmask will fail construction
        self.assertRaises(Exception, dyndnsc.detector.iface.IPDetector_Iface, {'netmask': 'fubar'})

    def test_teredo_detector(self):
        import dyndnsc.detector.teredo
        NAME = "teredo"
        self.assertEqual(NAME, dyndnsc.detector.teredo.IPDetector_Teredo.getName())
        detector = dyndnsc.detector.teredo.IPDetector_Teredo()
        self.assertTrue(detector.can_detect_offline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertNotEqual(None, detector.netmask)

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
        self.assertFalse(detector.can_detect_offline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
