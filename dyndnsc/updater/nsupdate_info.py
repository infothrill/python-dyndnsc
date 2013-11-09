# -*- coding: utf-8 -*-
"""
Updater for nsupdate.info dynamic dns service (which is dyndns2 compatible,
so this module is mostly for the sake of a different _updateurl and docs).

To avoid SSL certificate issues when using https, using Python >= 3.2 is
strongly recommended (SSL with SNI is painful with requests on Python 2.x).

Updating IPv4 (uses web based ip autodetection):
dyndnsc --hostname test.nsupdate.info \
        --userid   test.nsupdate.info --password xxxxxxxxxx \
        --protocol nsupdate \
        --loop --sleeptime 300 \
        --method=webcheck

Updating IPv6 (uses interface based ip detection):
dyndnsc --hostname test.nsupdate.info \
        --userid   test.nsupdate.info --password xxxxxxxxxx \
        --protocol nsupdate \
        --loop --sleeptime 300 \
        --method=Iface,netmask:2001:470:1234:5678::/64,iface:eth0,family:INET6
"""

from .base import UpdateProtocol


class UpdateProtocolNsUpdate(UpdateProtocol):
    """Protocol handler for nsupdate.info"""

    _updateurl = "https://nsupdate.info/nic/update"

    def __init__(self, options):
        self.theip = None
        self.hostname = options['hostname']
        self.userid = options['userid']
        self.password = options['password']

        super(UpdateProtocolNsUpdate, self).__init__()

    @staticmethod
    def configuration_key():
        return "nsupdate"

    def update(self, ip):
        self.theip = ip
        return self.protocol()
