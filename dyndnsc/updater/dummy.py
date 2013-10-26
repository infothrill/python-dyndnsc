# -*- coding: utf-8 -*-

from .base import UpdateProtocol


class UpdateProtocolDummy(UpdateProtocol):

    _updateurl = "http://localhost.nonexistant/nic/update"

    def __init__(self, options=None):
        if options is None:
            self._options = {}
        else:
            self._options = options
        super(UpdateProtocolDummy, self).__init__()

    @staticmethod
    def configuration_key():
        return "dummy"

    def update(self, ip):
        return ip
