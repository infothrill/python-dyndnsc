# -*- coding: utf-8 -*-

from .base import UpdateProtocol


class UpdateProtocolDyndns(UpdateProtocol):
    """Protocol handler for dyndns.com"""

    _updateurl = "https://members.dyndns.org/nic/update"

    def __init__(self, hostname, userid, password, **kwargs):
        self.hostname = hostname
        self.userid = userid
        self.password = password

        super(UpdateProtocolDyndns, self).__init__()

    @staticmethod
    def configuration_key():
        return "dyndns"

    def update(self, ip):
        self.theip = ip
        return self.protocol()
