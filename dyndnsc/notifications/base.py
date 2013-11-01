# -*- coding: utf-8 -*-

import logging
from abc import abstractmethod

log = logging.getLogger(__name__)


class Notification(object):

    default_title = "Dynamic DNS"

    def is_disabled(self):
        return not self.is_enabled()

    def is_enabled(self):
        return True  # TODO

    def create_notify_handler(self):
        return self._notify

    def _notify(self, *args, **kwargs):
        if self.is_enabled():
            return self.notify(*args, **kwargs)
        return False

    @abstractmethod
    def notify(self, caller, event, message):
        raise NotImplementedError("please implement in subclass")
