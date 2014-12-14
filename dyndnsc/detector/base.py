# -*- coding: utf-8 -*-

import logging
from socket import AF_INET, AF_INET6, AF_UNSPEC

from ..common.subject import Subject

log = logging.getLogger(__name__)


class IPDetector(Subject):
    """
    Base class for IP detectors. When implementing a new detector, it is
    usually best to just inherit from this class first.
    """
    def __init__(self, *args, **kwargs):
        """
        Default initializer for all detectors. Since we want to support ipv4
        and ipv6 in a concise manner, we make it a feature of the base class to
        handle these options.
        """
        super(IPDetector, self).__init__()

        self.opts_family = kwargs.get('family')
        # ensure address family is understood:
        af_ok = {None: AF_UNSPEC, 'INET': AF_INET, 'INET6': AF_INET6, AF_UNSPEC: AF_UNSPEC, AF_INET: AF_INET, AF_INET6: AF_INET6}
        if self.opts_family not in af_ok:
            raise ValueError("IPDetector(): Unsupported address family '%s' specified, please use one of %r" %
                             (self.opts_family, af_ok.keys()))
        else:
            self.opts_family = af_ok[self.opts_family]

    def can_detect_offline(self):
        """
        Must be overwritten in subclass. Return True if the IP detection
        does not generate any network traffic.
        """
        raise NotImplementedError("Abstract method, must be overridden")

    def af(self):
        """
        Might be overwritten in subclass. Returns the address family detected
        by this detector.
        """
        return self.opts_family

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
        if self._oldvalue != value:
            log.debug("%s.set_current_value(%s)", self.__class__.__name__, value)
        return value

    def has_changed(self):
        """Detect a state change with old and current value"""
        return self.get_old_value() != self.get_current_value()

    @staticmethod
    def names():
        raise NotImplementedError("Please implement in subclass")
