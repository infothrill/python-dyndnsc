# -*- coding: utf-8 -*-

"""
Main CLI program
"""

import sys
import logging

from dyndnsc import getDynDnsClientForConfig, __version__
from dyndnsc.daemon import daemonize
from dyndnsc.cli_helper import parse_cmdline_detector_args,\
    parse_cmdline_updater_args


def main():
    """
    The main. Initializes the stack, parses command line arguments, and fires
    requested logic.
    """
    from dyndnsc.plugins.manager import DefaultPluginManager
    plugins = DefaultPluginManager()
    plugins.load_plugins()
    from os import environ

    import argparse
    parser = argparse.ArgumentParser()

    # add the updater protocol options to the CLI:
    from dyndnsc.updater.manager import updater_classes
    for kls in updater_classes():
        kls.register_arguments(parser)

    # add the plugin options to the CLI:
    plugins.options(parser, environ)

    # add generic client options to the CLI:
    parser.add_argument("-c", "--config", dest="config",
                        help="config file", default=None)
    parser.add_argument("-d", "--daemon", dest="daemon",
                        help="go into daemon mode (implies --loop)",
                        action="store_true", default=False)
    parser.add_argument("--debug", dest="debug",
                        help="increase logging level to DEBUG",
                        action="store_true", default=False)
    parser.add_argument("--detector", "--method", dest="detector",
                        help="method for detecting your IP (default webcheck)",
                        default='webcheck')
    parser.add_argument("--loop", dest="loop",
                        help="loop forever (default is to update once)",
                        action="store_true", default=False)
    parser.add_argument("--sleeptime", dest="sleeptime",
                        help="how long to sleep between checks in seconds",
                        default=300)
    parser.add_argument("--version", dest="version",
                        help="show version and exit",
                        action="store_true", default=False)

    args = parser.parse_args()

    if args.version:
        print("dyndnsc %s" % __version__)
        return 0

    if args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)s %(message)s')
    # silence 'requests' logging
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    # we collect cmd line args, config file into a separate dict:
    collected_config = {}
    collected_config['sleeptime'] = int(args.sleeptime)

    if args.config:
        logging.debug(args.config)
        from dyndnsc.conf import getConfiguration, collect_config
        cfg = getConfiguration(args.config)
        more_conf = collect_config(cfg)
        collected_config.update(more_conf)
    else:
        collected_config['detector'] = parse_cmdline_detector_args(args.detector)
        collected_config['updaters'] = parse_cmdline_updater_args(args)

    plugins.configure(args)
    plugins.initialize()

    # done with command line options, bring on the dancing girls
    dyndnsclient = getDynDnsClientForConfig(collected_config, plugins=plugins)
    if dyndnsclient is None:
        return 1
    # do an initial synchronization, before going into endless loop:
    dyndnsclient.sync()

    if args.daemon:
        daemonize()  # fork into background
        args.loop = True

    if args.loop:
        dyndnsclient.loop()
    else:
        dyndnsclient.check()

    return 0

if __name__ == '__main__':
    sys.exit(main())
