'''
Created on Sep 27, 2013

@author: pk
'''

import unittest

from dyndnsc.notifier import osxnotificationcenter


class Test(unittest.TestCase):
    def test_notifications(self):
        # show a message instantly
        osxnotificationcenter.notify("Test message", "Subtitle", "This message should appear instantly, with a sound", sound=True)

        # show a message after 2 seconds
        osxnotificationcenter.notify("Another test", None, "This message appears after 2 seconds, without playing a sound", 2)
