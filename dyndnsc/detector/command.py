# -*- coding: utf-8 -*-

"""Module containing logic for command based detectors."""

from .base import IPDetector
from ..common.six import PY3


class IPDetector_Command(IPDetector):
    """IPDetector to detect IP address executing shell command/script."""

    def __init__(self, command="", *args, **kwargs):
        """
        Initializer.

        :param command: string shell command that writes IP address to STDOUT
        """
        super(IPDetector_Command, self).__init__(*args, **kwargs)

        self.opts_command = command

    @staticmethod
    def names():
        """Return a list of string names identifying this class/service."""
        return ("command",)

    def can_detect_offline(self):
        """Return false, as this detector possibly generates network traffic.

        :return: False
        """
        return False

    def setHostname(self, hostname):
        """Set the hostname."""
        self.hostname = hostname

    def detect(self):
        """Detect and return the IP address."""
        if PY3:  # py23
            import subprocess  # nosec @UnresolvedImport pylint: disable=import-error
        else:
            import commands as subprocess  # @UnresolvedImport pylint: disable=import-error
        try:
            theip = subprocess.getoutput(self.opts_command)  # nosec
        except Exception:
            theip = None
        self.set_current_value(theip)
        return theip
