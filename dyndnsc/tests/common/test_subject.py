# -*- coding: utf-8 -*-

"""Tests for the subject module."""

import unittest
import logging

from dyndnsc.common.subject import Subject


class SampleListener(object):
    """An example listener that records all notifications."""

    def __init__(self):
        """Initialize with an empty list of messages."""
        self.messages = []

    def notify(self, sender, event, msg):
        """Do nothing but remember the notification."""
        self.messages.append((sender, event, msg))


class InvalidListener(object):
    """An invalid listener."""

    def notify(self, dummy):
        """Do nothing."""
        pass


class TestSubjectObserver(unittest.TestCase):
    """Test cases for Subject."""

    def setUp(self):
        """Disable logging to not confuse the person watching the unit test output."""
        logging.disable(logging.CRITICAL)
        unittest.TestCase.setUp(self)

    def test_observer(self):
        """Run observer tests."""
        subject = Subject()
        subject.notify_observers("INVALID_EVENT", "msg")
        listener = SampleListener()
        subject.register_observer(listener.notify, ["SAMPLE_EVENT"])
        self.assertEqual(0, len(listener.messages))
        subject.notify_observers("INVALID_EVENT", "msg")
        self.assertEqual(0, len(listener.messages))
        subject.notify_observers("SAMPLE_EVENT", "msg")
        self.assertEqual(1, len(listener.messages))
        subject.notify_observers("SAMPLE_EVENT", "msg")
        self.assertEqual(2, len(listener.messages))
        self.assertEqual(1, len(subject._observers))
        subject.unregister_observer(listener.notify)
        self.assertEqual(0, len(subject._observers))
        subject.notify_observers("SAMPLE_EVENT", "msg")
        self.assertEqual(2, len(listener.messages))
        invalid_listener = InvalidListener()
        subject.register_observer(invalid_listener.notify, "FUNWITHFLAGS")
        self.assertEqual(1, len(subject._observers))
        subject.notify_observers("FUNWITHFLAGS", "msg")
        self.assertEqual(0, len(subject._observers))
