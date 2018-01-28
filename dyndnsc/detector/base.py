# -*- coding: utf-8 -*-

"""Module containing shared code for all detectors."""

import logging
from socket import AF_INET, AF_INET6, AF_UNSPEC

from ..common.subject import Subject
from ..common.dynamiccli import DynamicCliMixin

LOG = logging.getLogger(__name__)


class IPDetector(Subject, DynamicCliMixin):
    """
    Base class for IP detectors.

    When implementing a new detector, it is usually best to just inherit
    from this class first.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize detector.

        Since we want to support ipv4 and ipv6 in a concise manner, we make it
        a feature of the base class to handle these options.
        """
        super(IPDetector, self).__init__()

        self.opts_family = kwargs.get("family")
        # ensure address family is understood:
        af_ok = {None: AF_UNSPEC, "INET": AF_INET, "INET6": AF_INET6,
                 AF_UNSPEC: AF_UNSPEC, AF_INET: AF_INET, AF_INET6: AF_INET6}
        if self.opts_family not in af_ok:
            raise ValueError("IPDetector(): Unsupported address family '%s' specified, please use one of %r" %
                             (self.opts_family, af_ok.keys()))
        else:
            self.opts_family = af_ok[self.opts_family]

    def can_detect_offline(self):
        """
        Must be overwritten in subclass.

        Return True if the IP detection does not generate any network traffic.
        """
        raise NotImplementedError("Abstract method, must be overridden")

    def af(self):
        """
        Return the address family detected by this detector.

        Might be overwritten in subclass.
        """
        return self.opts_family

    def get_old_value(self):
        """Return the detected IP in the previous run (if any)."""
        try:
            return self._oldvalue
        except AttributeError:
            return self.get_current_value()

    def set_old_value(self, value):
        """Set the previously detected IP."""
        self._oldvalue = value

    def get_current_value(self, default=None):
        """Return the detected IP in the current run (if any)."""
        try:
            return self._currentvalue
        except AttributeError:
            return default

    def set_current_value(self, value):
        """Set the detected IP in the current run (if any)."""
        self._oldvalue = self.get_current_value()
        self._currentvalue = value
        if self._oldvalue != value:
            # self.notify_observers("new_ip_detected", {"ip": value})
            LOG.debug("%s.set_current_value(%s)", self.__class__.__name__, value)
        return value

    def has_changed(self):
        """Detect difference between old and current value."""
        return self.get_old_value() != self.get_current_value()

    @staticmethod
    def configuration_key_prefix():
        """Return "detector"."""
        return "detector"
