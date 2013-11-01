# -*- coding: utf-8 -*-

import logging

import gntp.notifier

from ..base import Notification

log = logging.getLogger(__name__)


class Growl(Notification):

    def notify(self, caller, event, message):
        gntp.notifier.mini(
            description=message,
            applicationName='dyndnsc',
            title=self.default_title,
            sticky=False,
            )
        return True
