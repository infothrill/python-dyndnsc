# -*- coding: utf-8 -*-

"""Module for growl notification."""

import gntp.notifier  # @UnresolvedImport pylint: disable=import-error

from ..base import Plugin


class Growl(object):
    """The Growl notifier."""

    default_title = "Dynamic DNS"
    application_name = "dyndnsc"

    def notify(self, caller, event, message):
        """
        Send a notification.

        :param caller: string caller
        :param event: string event
        :param message: string message
        """
        gntp.notifier.mini(
            description=message,
            applicationName=self.application_name,
            title=self.default_title,
            sticky=False,
        )
        return True


class GrowlPlugin(Plugin):
    """Send desktop notifications with Growl."""

    name = "growl"
    can_configure = True

    def initialize(self):
        """Initialize."""
        self.growl = Growl()

    def after_remote_ip_update(self, ip, status):
        """
        Handle the after_remote_ip_update plugin hook.

        :param ip: ip address
        :param status: string
        """
        if status == 0:
            self.growl.notify(self, None, "Remote IP updated to %s" % ip)
        else:
            self.growl.notify(self, None, "Problem updating remote IP to %s" % ip)
