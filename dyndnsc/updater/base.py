# -*- coding: utf-8 -*-

"""Module providing base class and functionality for all update protocols."""

import logging

from ..common.subject import Subject
from ..common.dynamiccli import DynamicCliMixin

LOG = logging.getLogger(__name__)


class UpdateProtocol(Subject, DynamicCliMixin):
    """Base class for all update protocols that use a simple http GET protocol."""

    theip = None
    __hostname = None  # private place to store the property 'hostname'
    configuration_key = None

    @property
    def hostname(self):
        """
        Return the hostname managed by this updater.

        May be implemented or overwritten in updater subclasses.
        """
        return self.__hostname

    @hostname.setter
    def hostname(self, value):
        """
        Set the hostname managed by this updater.

        May be implemented or overwritten in updater subclasses.
        """
        self.__hostname = value

    @staticmethod
    def configuration_key_prefix():
        """
        Return a human readable string classifying this class as an updater.

        Should not be be implemented or overwritten in updater subclasses.
        """
        return "updater"

    def update(self, ip):
        """
        Update the hostname on the remote service.

        Abstract method, must be implemented in subclass.
        """
        raise NotImplementedError("Please implement in subclass")
