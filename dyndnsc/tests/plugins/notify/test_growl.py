import unittest


class TestGrowlPlugin(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_growl(self):
        try:
            from dyndnsc.plugins.notify import growl
        except ImportError:
            pass
        else:
            plugin = growl.GrowlPlugin()
            plugin.initialize()
            plugin.after_remote_ip_update("127.0.0.1", status=0)
