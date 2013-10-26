# -*- coding: utf-8 -*-

from .base import IPDetector


class IPDetector_Command(IPDetector):
    """IPDetector to detect IP adress executing shell command/script"""
    def __init__(self, options):
        """
        Constructor
        @param options: dictionary

        available options:

        command: shell command that writes IP address to STDOUT
        """
        self.opts = {'command': ''}
        for k in options.keys():
            #logging.debug("%s explicitly got option: %s -> %s", self.__class__.__name__, k, options[k])
            self.opts[k] = options[k]
        super(IPDetector_Command, self).__init__()

    @staticmethod
    def getName():
        return "command"

    def canDetectOffline(self):
        """Returns false, as this detector possibly generates network traffic"""
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
            theip = subprocess.getoutput(self.opts['command'])
        except:
            theip = None
        self.setCurrentValue(theip)
        return theip
