# -*- coding: utf-8 -*-

"""Main CLI program."""

import sys
import os
import logging
import time
import argparse
from functools import partial

from .plugins.manager import DefaultPluginManager
from .updater.manager import updater_classes
from .detector.manager import detector_classes
from .core import getDynDnsClientForConfig
from .conf import get_configuration, collect_config
from .common.dynamiccli import parse_cmdline_args


LOG = logging.getLogger(__name__)


def list_presets(cfg, out=sys.stdout):
    """Write a human readable list of available presets to out.

    :param cfg: ConfigParser instance
    :param out: file object to write to
    """
    for section in cfg.sections():
        if section.startswith("preset:"):
            out.write((section.replace("preset:", "")) + os.linesep)
            for k, v in cfg.items(section):
                out.write("\t%s = %s" % (k, v) + os.linesep)


def create_argparser():
    """Instantiate an `argparse.ArgumentParser`.

    Adds all basic cli options including default values.
    """
    parser = argparse.ArgumentParser()
    arg_defaults = {
        "daemon": False,
        "loop": False,
        "listpresets": False,
        "config": None,
        "debug": False,
        "sleeptime": 300,
        "version": False,
        "verbose_count": 0
    }

    # add generic client options to the CLI:
    parser.add_argument("-c", "--config", dest="config",
                        help="config file", default=arg_defaults["config"])
    parser.add_argument("--list-presets", dest="listpresets",
                        help="list all available presets",
                        action="store_true", default=arg_defaults["listpresets"])
    parser.add_argument("-d", "--daemon", dest="daemon",
                        help="go into daemon mode (implies --loop)",
                        action="store_true", default=arg_defaults["daemon"])
    parser.add_argument("--debug", dest="debug",
                        help="increase logging level to DEBUG (DEPRECATED, please use -vvv)",
                        action="store_true", default=arg_defaults["debug"])
    parser.add_argument("--loop", dest="loop",
                        help="loop forever (default is to update once)",
                        action="store_true", default=arg_defaults["loop"])
    parser.add_argument("--sleeptime", dest="sleeptime",
                        help="how long to sleep between checks in seconds",
                        default=arg_defaults["sleeptime"])
    parser.add_argument("--version", dest="version",
                        help="show version and exit",
                        action="store_true", default=arg_defaults["version"])
    parser.add_argument("-v", "--verbose", dest="verbose_count",
                        action="count", default=arg_defaults["verbose_count"],
                        help="increases log verbosity for each occurrence")

    return parser, arg_defaults


def run_forever(dyndnsclients):
    """
    Run an endless loop accross the give dynamic dns clients.

    :param dyndnsclients: list of DynDnsClients
    """
    while True:
        try:
            # Do small sleeps in the main loop, needs_check() is cheap and does
            # the rest.
            time.sleep(15)
            for dyndnsclient in dyndnsclients:
                dyndnsclient.check()
        except (KeyboardInterrupt,):
            break
        except (Exception,) as exc:
            LOG.critical("An exception occurred in the dyndns loop", exc_info=exc)
    return 0


def main():
    """
    Run the main CLI program.

    Initializes the stack, parses command line arguments, and fires requested
    logic.
    """
    plugins = DefaultPluginManager()
    plugins.load_plugins()

    parser, _ = create_argparser()
    # add the updater protocol options to the CLI:
    for kls in updater_classes():
        kls.register_arguments(parser)

    for kls in detector_classes():
        kls.register_arguments(parser)

    # add the plugin options to the CLI:
    from os import environ
    plugins.options(parser, environ)

    args = parser.parse_args()

    if args.debug:
        args.verbose_count = 5  # some high number

    log_level = max(int(logging.WARNING / 10) - args.verbose_count, 0) * 10
    # print(log_level)
    logging.basicConfig(level=log_level, format="%(levelname)s %(message)s")
    # logging.debug("args %r", args)

    if args.version:
        from . import __version__
        print("dyndnsc %s" % __version__)  # noqa
        return 0

    # silence 'requests' logging
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    logging.debug(parser)
    cfg = get_configuration(args.config)

    if args.listpresets:
        list_presets(cfg)
        return 0

    if args.config:
        collected_configs = collect_config(cfg)
    else:
        parsed_args = parse_cmdline_args(args, updater_classes().union(detector_classes()))
        logging.debug("parsed_args %r", parsed_args)

        collected_configs = {
            "cmdline": {
                "interval": int(args.sleeptime)
            }
        }
        collected_configs["cmdline"].update(parsed_args)

    plugins.configure(args)
    plugins.initialize()

    logging.debug("collected_configs: %r", collected_configs)
    dyndnsclients = []
    for thisconfig in collected_configs:
        logging.debug("Initializing client for '%s'", thisconfig)
        # done with options, bring on the dancing girls
        dyndnsclient = getDynDnsClientForConfig(
            collected_configs[thisconfig], plugins=plugins)
        if dyndnsclient is None:
            return 1
        # do an initial synchronization, before going into endless loop:
        dyndnsclient.sync()
        dyndnsclients.append(dyndnsclient)

    run_forever_callable = partial(run_forever, dyndnsclients)

    if args.daemon:
        import daemonocle
        daemon = daemonocle.Daemon(worker=run_forever_callable)
        daemon.do_action("start")
        args.loop = True

    if args.loop:
        run_forever_callable()

    return 0


if __name__ == "__main__":
    sys.exit(main())
