# -*- coding: utf-8 -*-

import unittest

from dyndnsc.common.subject import Subject


class SampleListener(object):
    def __init__(self):
        self.messages = []

    def notify(self, sender, event, msg):
        self.messages.append((sender, event, msg))


class InvalidListener(object):
    def __init__(self):
        pass

    def notify(self, foo):
        pass


class SubjectObserverTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_observer(self):
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
        subject.register_observer(invalid_listener.notify, "FUNWITHERRORS")
        self.assertEqual(1, len(subject._observers))
        subject.notify_observers("FUNWITHERRORS", "msg")
        self.assertEqual(0, len(subject._observers))
