# -*- coding: utf-8 -*-

from .base import UpdateProtocol


class UpdateProtocolNoip(UpdateProtocol):
    """Protocol handler for www.noip.com"""

    _updateurl = "https://dynupdate.no-ip.com/nic/update"

    def __init__(self, options):
        self.theip = None
        self.hostname = options['hostname']
        self.userid = options['userid']
        self.password = options['password']

        super(UpdateProtocolNoip, self).__init__()

    @staticmethod
    def configuration_key():
        return "noip"

    def update(self, ip):
        self.theip = ip
        return self.protocol()
