# -*- coding: utf-8 -*-

"""
Helpers for the CLI program
"""

import logging

from .updater.manager import updater_classes

log = logging.getLogger(__name__)


def parse_cmdline_updater_args(args):
    """
    Parses out all updater related arguments from the entire args.

    Returns a list of ("updater_name", { "k": "v"})

    :param args: argparse arguments
    """
    if args is None:
        raise ValueError("args must not be None")
    updaters = []
    for kls in updater_classes():
        if getattr(args, 'updater_%s' % kls.configuration_key(), False):
            updater_name = kls.configuration_key()
            logging.debug(
                "Gathering initargs for '%s'", kls.configuration_key())
            updater_initargs = {}
            for arg_name in kls.init_argnames():
                val = getattr(args, 'updater_%s_%s' %
                              (kls.configuration_key(), arg_name))
                if val is not None:
                    updater_initargs[arg_name] = val
            updaters.append((updater_name, updater_initargs))
    return updaters


def parse_cmdline_detector_args(args_str):
    """
    Parses an options string into a detector name and an options dict.

    Example:
        "iface,family:INET" -> ("iface", {"family": "INET"})

    :param args_str: string
    """
    if args_str is None:
        raise ValueError("args must not be None")
    COMMA = ','
    COLON = ":"
    # allow opts to be a list or a comma-separated string:
    name, dummysep, opts = args_str.partition(COMMA)
    if len(name) == 0:
        raise ValueError(
            "detector name must not be empty (parsed from '%s')" % args_str)
    # make a dictionary from opts:
    options = {}
    for opt in opts.split(COMMA):
        if len(opt) == 0:
            break
        # options are key value pairs, separated by a COLON ":"
        # allow white-spaces in input, but strip them here:
        key, dummysep, value = opt.partition(COLON)
        key, value = key.strip(), value.strip()
        if key in options:
            log.warning("Option '%s' specified more than once, using '%s'.",
                        key, value)
        options[key] = value
    return name, options
