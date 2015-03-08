# -*- coding: utf-8 -*-

import logging

from ..common.subject import Subject
from ..common.dynamiccli import DynamicCliMixin

log = logging.getLogger(__name__)


class UpdateProtocol(Subject, DynamicCliMixin):

    """Base class for all update protocols that use a simple http GET protocol."""

    _updateurl = None
    theip = None
    hostname = None  # this holds the desired dns hostname

    def __init__(self):
        """Initializer."""
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
        Return a human readable string identifying the protocol.

        Must be implemented by all updater subclasses.
        """
        return "none_base_class"

    @staticmethod
    def configuration_key_prefix():
        """
        Return a human readable string classifying this class as an updater.

        Must be not be implemented or overwritten in updater subclasses.
        """
        return "updater"
