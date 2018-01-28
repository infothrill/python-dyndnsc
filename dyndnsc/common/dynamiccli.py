# -*- coding: utf-8 -*-

"""This module deals with dynamic CLI options."""

import logging
import textwrap

from .six import getargspec


def parse_cmdline_args(args, classes):
    """
    Parse all updater and detector related arguments from args.

    Returns a list of ("name", { "k": "v"})

    :param args: argparse arguments
    """
    if args is None:
        raise ValueError("args must not be None")
    parsed_args = {}
    for kls in classes:
        prefix = kls.configuration_key_prefix()
        name = kls.configuration_key
        if getattr(args, "%s_%s" % (prefix, name), False):
            logging.debug(
                "Gathering initargs for '%s.%s'", prefix, name)
            initargs = {}
            for arg_name in kls.init_argnames():
                val = getattr(args, "%s_%s_%s" %
                              (prefix, name, arg_name))
                if val is not None:
                    initargs[arg_name] = val
            if prefix not in parsed_args:
                parsed_args[prefix] = []
            parsed_args[prefix].append((name, initargs))
    return parsed_args


class DynamicCliMixin(object):
    """Base class providing functionality to register and handle CLI args."""

    @classmethod
    def init_argnames(cls):
        """
        Inspect the __init__ arguments of the given cls.

        :param cls: a class with an __init__ method
        """
        return getargspec(cls.__init__).args[1:]

    @classmethod
    def _init_argdefaults(cls):
        defaults = getargspec(cls.__init__).defaults
        if defaults is None:
            defaults = ()
        return defaults

    @classmethod
    def register_arguments(cls, parser):
        """Register command line options.

        Implement this method for normal options behavior with protection from
        OptionConflictErrors. If you override this method and want the default
        --$name option(s) to be registered, be sure to call super().
        """
        if hasattr(cls, "_dont_register_arguments"):
            return
        prefix = cls.configuration_key_prefix()
        cfgkey = cls.configuration_key
        parser.add_argument("--%s-%s" % (prefix, cfgkey),
                            action="store_true",
                            dest="%s_%s" % (prefix, cfgkey),
                            default=False,
                            help="%s: %s" %
                            (cls.__name__, cls.help()))
        args = cls.init_argnames()
        defaults = cls._init_argdefaults()
        for arg in args[0:len(args) - len(defaults)]:
            parser.add_argument("--%s-%s-%s" % (prefix, cfgkey, arg),
                                dest="%s_%s_%s" % (prefix, cfgkey, arg),
                                help="")
        for i, arg in enumerate(args[len(args) - len(defaults):]):
            parser.add_argument("--%s-%s-%s" % (prefix, cfgkey, arg),
                                dest="%s_%s_%s" % (prefix, cfgkey, arg),
                                default=defaults[i],
                                help="default: %(default)s")

    @classmethod
    def help(cls):
        """
        Return help for this.

        This will be output as the help section of the --$name option that
        enables this plugin.
        """
        if cls.__doc__:
            # remove doc section indentation
            return textwrap.dedent(cls.__doc__)
        return "(no help available)"

    @staticmethod
    def configuration_key_prefix():
        """
        Return string prefix for configuration key.

        Abstract method, must be implemented in subclass.
        """
        raise NotImplementedError("Please implement in subclass")
