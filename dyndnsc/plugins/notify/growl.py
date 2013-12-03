# -*- coding: utf-8 -*-

import gntp.notifier

from ..base import Plugin


class Growl(object):
    default_title = "Dynamic DNS"
    application_name = "dyndnsc"

    def notify(self, caller, event, message):
        gntp.notifier.mini(
            description=message,
            applicationName=self.application_name,
            title=self.default_title,
            sticky=False,
        )
        return True


class GrowlPlugin(Plugin):
    '''
    Send desktop notifications with Growl
    '''
    name = 'growl'
    can_configure = True

    def initialize(self):
        self.growl = Growl()

    def after_remote_ip_update(self, ip, status):
        if status == 0:
            self.growl.notify(self, None, "Remote IP updated to %s" % ip)
        else:
            self.growl.notify(self, None, "Problem updating remote IP to %s" % ip)
