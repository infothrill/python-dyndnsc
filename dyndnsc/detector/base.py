# -*- coding: utf-8 -*-

import logging
import warnings

from ..common.subject import Subject

log = logging.getLogger(__name__)


class IPDetector(Subject):
    """
    Base class for IP detectors. When implementing a new detector, it is
    usually best to just inherit from this class first.
    """
    def __init__(self, *args, **kwargs):
        super(IPDetector, self).__init__()

    def can_detect_offline(self):
        """
        Must be overwritten in subclass. Return True if the IP detection
        does not generate any network traffic.
        """
        raise NotImplementedError("Abstract method, must be overridden")

    def get_old_value(self):
        try:
            return self._oldvalue
        except AttributeError:
            return self.get_current_value()

    def set_old_value(self, value):
        self._oldvalue = value

    def get_current_value(self, default=None):
        try:
            return self._currentvalue
        except AttributeError:
            return default

    def set_current_value(self, value):
        self._oldvalue = self.get_current_value()
        self._currentvalue = value
        log.debug("%s.set_current_value(%s)", self.__class__.__name__, value)
        return value

    def has_changed(self):
        """Detect a state change with old and current value"""
        return self.get_old_value() != self.get_current_value()

    @staticmethod
    def names():
        raise NotImplementedError("Please implement in subclass")
