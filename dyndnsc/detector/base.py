# -*- coding: utf-8 -*-

from ..common.subject import Subject


class BaseClass(Subject):
    """A common base class providing logging and desktop-notification.
    """
    def __init__(self, *args, **kwargs):
        super(BaseClass, self).__init__()
        #from dyndnsc.notifier.macgrowl import notify
        #self.register_observer(notify)

    def emit(self, message):
        """
        sends message to the notifier
        """
        self.notify_observers(event='Dynamic DNS', msg=message)


class IPDetector(BaseClass):
    """
    Base class for IP detectors. Really is just a state machine for
    old/current value.
    """
    def __init__(self, *args, **kwargs):
        super(IPDetector, self).__init__()

    def canDetectOffline(self):
        """
        Must be overwritten. Return True when the IP detection can work
        offline without causing network traffic.
        """
        raise NotImplementedError("Abstract method, must be overridden")

    def getOldValue(self):
        if not '_oldvalue' in vars(self):
            self._oldvalue = self.getCurrentValue()
        return self._oldvalue

    def setOldValue(self, value):
        self._oldvalue = value

    def getCurrentValue(self, default=None):
        if not hasattr(self, '_currentvalue'):
            self._currentvalue = default
        return self._currentvalue

    def setCurrentValue(self, value):
        if value != self.getCurrentValue(value):
            self._oldvalue = self.getCurrentValue(value)
            self._currentvalue = value
            self.emit("new IP detected: %s" % str(value))
        return value

    def hasChanged(self):
        """Detect a state change with old and current value"""
        if self.getOldValue() == self.getCurrentValue():
            return False
        else:
            return True
