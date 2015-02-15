# -*- coding: utf-8 -*-

from .base import UpdateProtocol


class UpdateProtocolDummy(UpdateProtocol):

    _updateurl = "http://localhost.nonexistant/nic/update"
    _dont_register_arguments = True

    def __init__(self, hostname, **kwargs):
        self.hostname = hostname
        super(UpdateProtocolDummy, self).__init__()

    @staticmethod
    def configuration_key():
        return "dummy"

    def update(self, ip):
        return ip
