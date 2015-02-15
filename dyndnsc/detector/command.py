# -*- coding: utf-8 -*-

from .base import IPDetector


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
        return ("command",)

    def can_detect_offline(self):
        """Return false, as this detector possibly generates network traffic.

        :return: False
        """
        return False

    def setHostname(self, hostname):
        self.hostname = hostname

    def detect(self):
        import sys
        if sys.version_info >= (3, 0):
            import subprocess
        else:
            import commands as subprocess
        try:
            theip = subprocess.getoutput(self.opts_command)
        except:
            theip = None
        self.set_current_value(theip)
        return theip
