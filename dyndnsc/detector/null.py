# -*- coding: utf-8 -*-

import logging

from .base import IPDetector

log = logging.getLogger(__name__)


class IPDetector_Null(IPDetector):

    """Dummy IP detector."""

    def __init__(self, family=None, *args, **kwargs):
        """
        Initializer.

        :param family: IP address family (default: '' (ANY), also possible: 'INET', 'INET6')
        """
        super(IPDetector_Null, self).__init__(*args, family=family, **kwargs)

    @staticmethod
    def names():
        return ("null",)

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
