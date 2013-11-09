# -*- coding: utf-8 -*-

import logging
from abc import abstractmethod

log = logging.getLogger(__name__)


class Notification(object):

    default_title = "Dynamic DNS"

    def create_notify_handler(self):
        return self._notify

    def _notify(self, *args, **kwargs):
        return self.notify(*args, **kwargs)

    @abstractmethod
    def notify(self, caller, event, message):
        raise NotImplementedError("please implement in subclass")
