# -*- coding: utf-8 -*-

"""Module containing logic for command based detectors."""

from .base import IPDetector


class IPDetector_Command(IPDetector):
    """IPDetector to detect IP address executing shell command/script."""

    configuration_key = "command"

    def __init__(self, command="", *args, **kwargs):
        """
        Initialize.

        :param command: string shell command that writes IP address to STDOUT
        """
        super(IPDetector_Command, self).__init__(*args, **kwargs)

        self.opts_command = command

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
        import subprocess  # noqa: S404 @UnresolvedImport pylint: disable=import-error
        try:
            theip = subprocess.getoutput(self.opts_command)  # noqa: S605
        except Exception:
            theip = None
        self.set_current_value(theip)
        return theip
