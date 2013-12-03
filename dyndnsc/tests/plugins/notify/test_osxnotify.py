import unittest


class TestOSXNotify(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_osxnotify(self):
        try:
            from dyndnsc.plugins.notify import osxnotify
        except ImportError:
            pass
        else:
            plugin = osxnotify.OSXNotifyPlugin()
            plugin.initialize()
            plugin.after_remote_ip_update("127.0.0.1", status=0)
