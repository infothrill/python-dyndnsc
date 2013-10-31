# -*- coding: utf-8 -*-

"""
Example CLI program
"""

import sys
import os
import pkg_resources
import logging

from dyndnsc import getDynDnsClientForConfig


def daemonize(stdout='/dev/null', stderr=None, stdin=os.devnull,
              pidfile=None, startmsg='started with pid %s'):
    """
        This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        These arguments are optional and default to /dev/null.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.
    """
    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent.
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s%s" % (e.errno, e.strerror, os.linesep))
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # interestingly enough, we MUST open STDOUT explicitly before we
    # fork the second time.
    # Otherwise, the duping of sys.stdout won't work,
    # and we will not be able to capture stdout
    sys.stdout.write('')

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent.
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s%s" % (e.errno, e.strerror, os.linesep))
        sys.exit(1)

    # Open file descriptors and print start message
    if not stderr:
        stderr = stdout
    si = open(stdin, 'rb')
    so = open(stdout, 'w+b')
    se = open(stderr, 'w+b', 0)
    pid = str(os.getpid())
    sys.stderr.write("%s%s" % (startmsg, os.linesep) % pid)
    sys.stderr.flush()
    if pidfile:
        open(pidfile, 'w+b').write("%s%s" % (pid, os.linesep))

    # Redirect standard file descriptors.
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daemon", dest="daemon", help="go into daemon mode (implies --loop)", action="store_true", default=False)
    parser.add_argument("--hostname", dest="hostname", help="hostname to update", default=None)
    parser.add_argument("--key", dest="key", help="your authentication key", default=None)
    parser.add_argument("--userid", dest="userid", help="your userid", default=None)
    parser.add_argument("--password", dest="password", help="your password", default=None)
    parser.add_argument("--protocol", dest="protocol", help="protocol/service to use for updating your IP (default dyndns)", default='dyndns')
    parser.add_argument("--method", dest="method", help="method for detecting your IP (default webcheck)", default='webcheck')
    parser.add_argument("--loop", dest="loop", help="loop forever (default is to update once)", action="store_true", default=False)
    parser.add_argument("--sleeptime", dest="sleeptime", help="how long to sleep between checks in seconds", default=300)
    parser.add_argument("--version", dest="version", help="show version and exit", action="store_true", default=False)
    args = parser.parse_args()

    if args.version:
        print("dyndnsc %s" % pkg_resources.get_distribution("dyndnsc").version)  # pylint: disable=E1103
        return 0

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

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
