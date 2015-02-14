# -*- coding: utf-8 -*-

import logging
import textwrap
from socket import AF_INET, AF_INET6, AF_UNSPEC

from ..common.subject import Subject

log = logging.getLogger(__name__)


class IPDetector(Subject):

    """
    Base class for IP detectors.

    When implementing a new detector, it is usually best to just inherit
    from this class first.
    """

    def __init__(self, *args, **kwargs):
        """
        Default initializer for all detectors.

        Since we want to support ipv4 and ipv6 in a concise manner, we make it
        a feature of the base class to handle these options.
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
            log.debug("%s.set_current_value(%s)", self.__class__.__name__, value)
        return value

    def has_changed(self):
        """Detect a state change with old and current value"""
        return self.get_old_value() != self.get_current_value()

    @staticmethod
    def names():
        raise NotImplementedError("Please implement in subclass")

    @classmethod
    def init_argnames(cls):
        import inspect
        return inspect.getargspec(cls.__init__).args[1:]

    @classmethod
    def _init_argdefaults(cls):
        import inspect
        defaults = inspect.getargspec(cls.__init__).defaults
        if defaults is None:
            defaults = ()
        return defaults

    @classmethod
    def register_arguments(cls, parser):
        """Register commandline options.

        Implement this method for normal options behavior with protection from
        OptionConflictErrors. If you override this method and want the default
        --updater-$name option(s) to be registered, be sure to call super().
        """
        if hasattr(cls, '_dont_register_arguments'):
            return
        cfgkey = cls.names()[-1]
        parser.add_argument("--detector-%s" % cfgkey,
                            action="store_true",
                            dest="detector_%s" % cfgkey,
                            default=False,
                            help="Use detector %s: %s" %
                            (cls.__name__, cls.help()))
        args = cls.init_argnames()
        defaults = cls._init_argdefaults()
        for arg in args[0:len(args) - len(defaults)]:
            parser.add_argument("--detector-%s-%s" % (cfgkey, arg),
                                dest="detector_%s_%s" % (cfgkey, arg),
                                help="")
        for i, arg in enumerate(args[len(args) - len(defaults):]):
            parser.add_argument("--detector-%s-%s" % (cfgkey, arg),
                                dest="detector_%s_%s" % (cfgkey, arg),
                                default=defaults[i],
                                help="default: %(default)s")

    @classmethod
    def help(cls):
        """Return help for this protocol updater. This will be output as the
        help section of the --updater-$name option that enables this plugin.
        """
        if cls.__doc__:
            # remove doc section indentation
            return textwrap.dedent(cls.__doc__)
        return "(no help available)"
