# -*- coding: utf-8 -*-

import logging
import textwrap

from ..common.subject import Subject

log = logging.getLogger(__name__)


class UpdateProtocol(Subject):
    """
    base class for all update protocols that use the dyndns2 update protocol
    """

    _updateurl = None
    theip = None
    hostname = None  # this holds the desired dns hostname

    def __init__(self):
        self.updateurl = self._updateurl
        super(UpdateProtocol, self).__init__()

    def updateUrl(self):
        return self.updateurl

    def service_url(self):
        return self.updateUrl()

    @staticmethod
    def configuration_key():
        """
        This method must be implemented by all updater subclasses. Returns a
        human readable string identifying the protocol.
        """
        return "none_base_class"

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
        cfgkey = cls.configuration_key()
        parser.add_argument("--updater-%s" % cfgkey,
                            action="store_true",
                            dest="updater_%s" % cfgkey,
                            default=False,
                            help="Use updater %s: %s" %
                            (cls.__name__, cls.help()))
        args = cls.init_argnames()
        defaults = cls._init_argdefaults()
        for arg in args[0:len(args) - len(defaults)]:
            parser.add_argument("--updater-%s-%s" % (cfgkey, arg),
                                dest="updater_%s_%s" % (cfgkey, arg),
                                help="")
        for i, arg in enumerate(args[len(args) - len(defaults):]):
            parser.add_argument("--updater-%s-%s" % (cfgkey, arg),
                                dest="updater_%s_%s" % (cfgkey, arg),
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
