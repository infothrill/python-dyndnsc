# -*- coding: utf-8 -*-

"""Module providing a dummy updater."""

from .base import UpdateProtocol


class UpdateProtocolDummy(UpdateProtocol):
    """The dummy update protocol."""

    _updateurl = "http://localhost.nonexistant/nic/update"
    _dont_register_arguments = True

    def __init__(self, hostname, **kwargs):
        """
        Initialize.

        :param hostname: string hostname
        """
        self.hostname = hostname
        super(UpdateProtocolDummy, self).__init__()

    @staticmethod
    def configuration_key():
        """Return 'dummy', identifying the protocol."""
        return "dummy"

    def update(self, ip):
        """Pretend to update the IP on the remote service."""
        return ip
