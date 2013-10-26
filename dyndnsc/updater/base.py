# -*- coding: utf-8 -*-

import requests

from ..common.subject import Subject


class BaseClass(Subject):
    """A common base class providing logging and desktop-notification.
    """
    def emit(self, message):
        """
        sends message to the notifier
        """
        self.notify_observers(event='Dynamic DNS', msg=message)


class UpdateProtocol(BaseClass):
    """the base class for all update protocols"""

    _updateurl = None
    theip = None
    hostname = None  # this holds the desired dns hostname
    status = 0
    nochgcount = 0
    failcount = 0

    def __init__(self):
        self.updateurl = self._updateurl
        super(UpdateProtocol, self).__init__()

    def updateUrl(self):
        return self.updateurl

    def success(self):
        self.status = 0
        self.failcount = 0
        self.nochgcount = 0
        #self.emit("Updated IP address of '%s' to %s" % (self.hostname, self.theip))

    def abuse(self):
        self.status = 1
        self.failcount = 0
        self.nochgcount = 0
        #self.emit("This client is considered to be abusive for hostname '%s'" % (self.hostname))

    def nochg(self):
        self.status = 0
        self.failcount = 0
        self.nochgcount += 1

    def nohost(self):
        self.status = 1
        self.failcount += 1
        self.emit("Invalid/non-existant hostname: [%s]" % (self.hostname))
        self.status = "nohost"

    def failure(self):
        self.status = 1
        self.failcount += 1
        self.emit("Service is failing!")

    def notfqdn(self):
        self.status = 1
        self.failcount += 1
        self.emit("The provided hostname '%s' is not a valid hostname!" % (self.hostname))

    def protocol(self):
        if hasattr(self, '_protocol'):
            return self._protocol()

        params = {'myip': self.theip, 'hostname': self.hostname}
        r = requests.get(self.updateUrl(), params=params, auth=(self.userid, self.password))
        if r.status_code == 200:
            if r.text.startswith("good "):
                self.success()
                return self.theip
            elif r.text == 'nochg':
                self.nochg()
                return self.theip
            elif r.text == 'nohost':
                self.nohost()
                return 'nohost'
            elif r.text == 'abuse':
                self.abuse()
                return 'abuse'
            elif r.text == '911':
                self.failure()
                return '911'
            elif r.text == 'notfqdn':
                self.notfqdn()
                return 'notfqdn'
            else:
                self.status = 1
                self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.text))
                return r.text
        else:
            self.status = 1
            self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.status_code))
            return 'invalid http status code: %s' % r.status_code

