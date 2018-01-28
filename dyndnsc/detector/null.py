# -*- coding: utf-8 -*-

"""Module containing logic for null detector."""

import logging

from .base import IPDetector

LOG = logging.getLogger(__name__)


class IPDetector_Null(IPDetector):
    """Dummy IP detector."""

    configuration_key = "null"

    def __init__(self, family=None, *args, **kwargs):
        """
        Initializer.

        :param family: IP address family (default: '' (ANY), also possible: 'INET', 'INET6')
        """
        super(IPDetector_Null, self).__init__(*args, family=family, **kwargs)

    def can_detect_offline(self):
        """Return true, as this detector generates no network traffic.

        :return: True
        """
        return True

    def detect(self):
        """
        Return None.

        :rtype: None
        """
        return None
