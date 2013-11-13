# -*- coding: utf-8 -*-

"""
Example CLI program
"""

import sys
import pkg_resources
import logging

from dyndnsc import getDynDnsClientForConfig
from dyndnsc.daemon import daemonize


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemon", dest="daemon",
                        help="go into daemon mode (implies --loop)",
                        action="store_true", default=False)
    parser.add_argument("--debug", dest="debug",
                        help="increase logging level to DEBUG",
                        action="store_true", default=False)
    parser.add_argument("--hostname", dest="hostname",
                        help="hostname to update", default=None)
    parser.add_argument("--key", dest="key",
                        help="your authentication key", default=None)
    parser.add_argument("--userid", dest="userid",
                        help="your userid", default=None)
    parser.add_argument("--password", dest="password",
                        help="your password", default=None)
    parser.add_argument("--protocol", dest="protocol",
                        help="protocol to use for updating IP (default dyndns)",
                        default='dyndns')
    parser.add_argument("--method", dest="method",
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
        print("dyndnsc %s" % pkg_resources.get_distribution("dyndnsc").version)  # pylint: disable=E1103
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

    if args.hostname is None:
        parser.error("Please specify a hostname using --hostname")

    config = {}
    config['hostname'] = args.hostname
    config['key'] = args.key
    config['userid'] = args.userid
    config['password'] = args.password
    config['protocol'] = args.protocol
    config['method'] = args.method
    config['sleeptime'] = int(args.sleeptime)

    # done with command line options, bring on the dancing girls
    dyndnsclient = getDynDnsClientForConfig(config)
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
