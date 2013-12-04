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

    def canDetectOffline(self):
        warnings.warn("canDetectOffline is deprecated; use "
               "can_detect_offline() instead", DeprecationWarning, stacklevel=2)
        return self.can_detect_offline()

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

    def getOldValue(self):
        warnings.warn("getOldValue is deprecated; use get_old_value() "
              "instead", DeprecationWarning, stacklevel=2)
        return self.get_old_value()

    def set_old_value(self, value):
        self._oldvalue = value

    def setOldValue(self, value):
        warnings.warn("setOldValue is deprecated; use set_old_value() "
              "instead", DeprecationWarning, stacklevel=2)
        self.set_old_value(value)

    def get_current_value(self, default=None):
        try:
            return self._currentvalue
        except AttributeError:
            return default

    def getCurrentValue(self, default=None):
        warnings.warn("getCurrentValue is deprecated; use get_current_value() "
              "instead", DeprecationWarning, stacklevel=2)
        return self.get_current_value(default)

    def set_current_value(self, value):
        self._oldvalue = self.get_current_value()
        self._currentvalue = value
        log.debug("%s.set_current_value(%s)", self.__class__.__name__, value)
        return value

    def setCurrentValue(self, value):
        warnings.warn("setCurrentValue is deprecated; use set_current_value() "
              "instead", DeprecationWarning, stacklevel=2)
        return self.set_current_value(value)

    def has_changed(self):
        """Detect a state change with old and current value"""
        return self.get_old_value() != self.get_current_value()

    def hasChanged(self):
        warnings.warn("hasChanged is deprecated; use has_changed() "
              "instead", DeprecationWarning, stacklevel=2)
        return self.has_changed()

    @classmethod
    def getName(cls):
        warnings.warn("getName() is deprecated; use names() "
              "instead", DeprecationWarning, stacklevel=2)
        return cls.names()[0]

    @staticmethod
    def names():
        raise NotImplementedError("Please implement in subclass")
