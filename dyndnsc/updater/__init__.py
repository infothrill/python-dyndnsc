# -*- coding: utf-8 -*-

import requests


class BaseClass(object):
    """A common base class providing logging and desktop-notification.
    """
    def registerNotifier(self, notifier):
        self.notifier = notifier

    def emit(self, message):
        """
        sends message to the notifier
        """
        try:
            self.notifier('Dynamic DNS', str(message))
        except:
            pass


class UpdateProtocol(BaseClass):
    """the base class for all update protocols"""
    hostname = None  # this holds the desired dns hostname
    status = 0
    nochgcount = 0
    failcount = 0

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


class UpdateProtocolMajimoto(UpdateProtocol):
    """This class contains the logic for talking to the update service of dyndns.majimoto.net"""
    def __init__(self, protocol_options):
        for k in ['key', 'hostname']:
            assert k in protocol_options, "Protocol option '%s' is missing" % k
            assert protocol_options[k] is not None, "Protocol option '%s' is not set" % k
            assert type(protocol_options[k]) == type(""), "Protocol option '%s' is not a string" % k

        self.key = protocol_options['key']
        self.hostname = protocol_options['hostname']
        self.theip = None

        self.failcount = 0
        self.nochgcount = 0

    def update(self, ip):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        params = {'myip': self.theip, 'key': self.key, 'hostname': self.hostname}
        r = requests.get(self.updateUrl(), params=params)
        if r.status_code == 200:
            if r.text == 'good':
                self.success()
            elif r.text == 'nochg':
                self.nochg()
            elif r.text == 'nohost':
                self.nohost()
            elif r.text == 'abuse':
                self.abuse()
            elif r.text == '911':
                self.failure()
            elif r.text == 'notfqdn':
                self.notfqdn()
            else:
                self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.text))
        else:
            self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.status_code))

    @staticmethod
    def configuration_key():
        return "majimoto"

    @staticmethod
    def updateUrl():
        return "https://dyndns.majimoto.net/nic/update"


class UpdateProtocolDyndns(UpdateProtocol):
    """Protocol handler for dyndns.com"""

    def __init__(self, protocol_options):
        for k in ['hostname', 'userid', 'password']:
            assert k in protocol_options, "Protocol option '%s' is missing" % k
            assert protocol_options[k] is not None, "Protocol option '%s' is not set" % k
            assert type(protocol_options[k]) == type(""), "Protocol option '%s' is not a string" % k

        self.theip = None
        self.hostname = protocol_options['hostname']
        self.userid = protocol_options['userid']
        self.password = protocol_options['password']

        self.failcount = 0
        self.nochgcount = 0

    @staticmethod
    def configuration_key():
        return "dyndns"

    @staticmethod
    def updateUrl():
        return "https://members.dyndns.org/nic/update"

    def update(self, ip):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        params = {'myip': self.theip, 'hostname': self.hostname}
        r = requests.get(self.updateUrl(), params=params, auth=(self.userid, self.password))
        if r.status_code == 200:
            if r.text == 'good':
                self.success()
            elif r.text == 'nochg':
                self.nochg()
            elif r.text == 'nohost':
                self.nohost()
            elif r.text == 'abuse':
                self.abuse()
            elif r.text == '911':
                self.failure()
            elif r.text == 'notfqdn':
                self.notfqdn()
            else:
                self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.text))
        else:
            self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.status_code))


class UpdateProtocolNoip(UpdateProtocol):
    """Protocol handler for www.noip.com"""

    def __init__(self, protocol_options):
        for k in ['hostname', 'userid', 'password']:
            assert k in protocol_options, "Protocol option '%s' is missing" % k
            assert protocol_options[k] is not None, "Protocol option '%s' is not set" % k
            assert type(protocol_options[k]) == type(""), "Protocol option '%s' is not a string" % k

        self.theip = None
        self.hostname = protocol_options['hostname']
        self.userid = protocol_options['userid']
        self.password = protocol_options['password']

        self.status = 0
        self.failcount = 0
        self.nochgcount = 0

    @staticmethod
    def configuration_key():
        return "noip"

    @staticmethod
    def updateUrl():
        return "https://dynupdate.no-ip.com/nic/update"

    def update(self, ip):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        params = {'myip': self.theip, 'hostname': self.hostname}
        r = requests.get(self.updateUrl(), params=params, auth=(self.userid, self.password))
        if r.status_code == 200:
            if r.text.startswith("good "):
                self.success()
            elif r.text == 'nochg':
                self.nochg()
            elif r.text == 'nohost':
                self.nohost()
            elif r.text == 'abuse':
                self.abuse()
            elif r.text == '911':
                self.failure()
            elif r.text == 'notfqdn':
                self.notfqdn()
            else:
                self.status = 1
                self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.text))
        else:
            self.status = 1
            self.emit("Problem updating IP address of '%s' to %s: %s" % (self.hostname, self.theip, r.status_code))
