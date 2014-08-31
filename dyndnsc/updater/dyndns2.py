# -*- coding: utf-8 -*-

import sys
from logging import getLogger

from .base import UpdateProtocol

import requests

log = getLogger(__name__)


class UpdateProtocolDyndns2(UpdateProtocol):
    """Updater for services compatible with dyndns.com"""

    def __init__(self, hostname, userid, password,
                 service_url="https://members.dyndns.org/nic/update", **kwargs):
        '''
        :param hostname: the fully qualified hostname to be managed
        :param userid: the userid for identification
        :param password: the password for authentication
        '''
        self.hostname = hostname
        self.userid = userid
        self.password = password
        self._updateurl = service_url

        if sys.version_info < (3, 2) and service_url.startswith("https://nsupdate.info/"):
            log.warn("""To avoid SSL certificate issues when using https://nsupdate.info/, using Python >= 3.2 is strongly recommended (SSL with SNI is painful with requests on Python 2.x)""")

        super(UpdateProtocolDyndns2, self).__init__()

    @staticmethod
    def configuration_key():
        return "dyndns2"

    def update(self, ip):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        timeout = 60
        log.debug("Updating '%s' to '%s' at service '%s'", self.hostname, self.theip, self.updateUrl())
        params = {'myip': self.theip, 'hostname': self.hostname}
        try:
            r = requests.get(self.updateUrl(), params=params,
                             auth=(self.userid, self.password), timeout=timeout)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            log.warning("an error occurred while updating IP at '%s'",
                        timeout, self.updateUrl(), exc_info=exc)
            return False
        else:
            r.close()
        log.debug("status %i, %s", r.status_code, r.text)
        if r.status_code == 200:
            if r.text.startswith("good "):
                return self.theip
            elif r.text.startswith('nochg'):
                return self.theip
            elif r.text == 'nohost':
                return 'nohost'
            elif r.text == 'abuse':
                return 'abuse'
            elif r.text == '911':
                return '911'
            elif r.text == 'notfqdn':
                return 'notfqdn'
            else:
                return r.text
        else:
            return 'invalid http status code: %s' % r.status_code


class UpdateProtocolNsUpdate(UpdateProtocolDyndns2):
    """
    Updater for nsupdate.info dynamic dns service (which is dyndns2 compatible,
    so this class is only here for the sake of a different service_url).

    To avoid SSL certificate issues when using https, using Python >= 3.2 is
    strongly recommended (SSL with SNI is painful with requests on Python 2.x).
    """

    def __init__(self, hostname, userid, password,
                 service_url="https://nsupdate.info/nic/update", **kwargs):

        super(UpdateProtocolNsUpdate, self).__init__(hostname, userid, password,
                                                 service_url, **kwargs)

        if sys.version_info < (3, 2) and service_url.startswith("https://nsupdate.info/"):
            log.warn("""To avoid SSL certificate issues when using https://nsupdate.info/, using Python >= 3.2 is strongly recommended (SSL with SNI is painful with requests on Python 2.x)""")

    @staticmethod
    def configuration_key():
        return "nsupdate"


class UpdateProtocolNoip(UpdateProtocolDyndns2):
    """Protocol handler for www.noip.com, behaves exactly like dyndns2 but
    this point to a different default service_url"""

    def __init__(self, hostname, userid, password,
                 service_url="https://dynupdate.no-ip.com/nic/update",
                 **kwargs):

        super(UpdateProtocolNoip, self).__init__(hostname, userid, password,
                                                 service_url, **kwargs)

    @staticmethod
    def configuration_key():
        return "noip"
