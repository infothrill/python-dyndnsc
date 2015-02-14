# -*- coding: utf-8 -*-

import logging

from ..common.subject import Subject
from ..common.dynamiccli import DynamicCliMixin

log = logging.getLogger(__name__)


class UpdateProtocol(Subject, DynamicCliMixin):
    """
    base class for all update protocols that use the dyndns2 update protocol
    """

    _updateurl = None
    theip = None
    hostname = None  # this holds the desired dns hostname

    def __init__(self):
        self.updateurl = self._updateurl
        super(UpdateProtocol, self).__init__()

    def updateUrl(self):
        return self.updateurl

    def service_url(self):
        return self.updateUrl()

    def url(self):
        return self.updateUrl()

    @staticmethod
    def configuration_key():
        """
        This method must be implemented by all updater subclasses. Returns a
        human readable string identifying the protocol.
        """
        return "none_base_class"

    @staticmethod
    def configuration_key_prefix():
        return "updater"
