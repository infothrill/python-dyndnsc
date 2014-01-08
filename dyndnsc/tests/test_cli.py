import unittest


class TestCli(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testCli(self):
        # all we do here is import code, no running...
        from dyndnsc import cli
