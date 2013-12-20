# -*- coding: utf-8 -*-

from .base import UpdateProtocol


class UpdateProtocolNoip(UpdateProtocol):
    """Protocol handler for www.noip.com"""

    _updateurl = "https://dynupdate.no-ip.com/nic/update"

    def __init__(self, hostname, userid, password, **kwargs):
        self.hostname = hostname
        self.userid = userid
        self.password = password

        self.theip = None

        super(UpdateProtocolNoip, self).__init__()

    @staticmethod
    def configuration_key():
        return "noip"

    def update(self, ip):
        self.theip = ip
        return self.protocol()
