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


def parse_cmdline_detector_args(detargs):
    """
    parse an options string (or list) into the detector name and an options dict
    Example:
        "iface,family:INET" -> ("iface", {"family": "INET"})

    :param detargs: string
    """
    if detargs is None:
        raise ValueError("args must not be None")
    # allow opts to be a list or a comma-separated string:
    if type(detargs) != list:
        detargs = detargs.split(',')
    name, opts = detargs[0], detargs[1:]
    if name == '':
        raise ValueError("The detector name must not be empty (parsed from '%s')" % ",".join(detargs))
    # make a dictionary from opts:
    options = {}
    colon = ":"
    for opt in opts:
        # options are key value pairs, separated by a colon ":"
        # allow white-spaces in input, but strip them here:
        key, dummysep, value = opt.partition(colon)
        key, value = key.strip(), value.strip()
        if key in options:
            log.warning("Option '%s' specified more than once, using '%s'.",
                        key, value)
        options[key] = value
    return name, options
