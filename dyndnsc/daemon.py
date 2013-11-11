# -*- coding: utf-8 -*-

"""
module containing logic to run the dyndnsc cli program as a UNIX daemon
"""

import sys
import os


def daemonize(stdout=os.devnull, stderr=None, stdin=os.devnull,
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
