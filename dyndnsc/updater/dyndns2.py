# -*- coding: utf-8 -*-

from logging import getLogger

from .base import UpdateProtocol
from ..common import constants

import requests

log = getLogger(__name__)


class UpdateProtocolDyndns2(UpdateProtocol):
    """Updater for services compatible with the dyndns2 protocol."""

    def __init__(self, hostname, userid, password, url, *args, **kwargs):
        """
        :param hostname: the fully qualified hostname to be managed
        :param userid: the userid for identification
        :param password: the password for authentication
        :param url: the API URL for updating the DNS entry
        """
        self.hostname = hostname
        self.userid = userid
        self.password = password
        self._updateurl = url

        super(UpdateProtocolDyndns2, self).__init__()

    @staticmethod
    def configuration_key():
        return "dyndns2"

    def update(self, ip):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        timeout = 60
        log.debug("Updating '%s' to '%s' at service '%s'", self.hostname, self.theip, self.url())
        params = {'myip': self.theip, 'hostname': self.hostname}
        try:
            r = requests.get(self.updateUrl(), params=params, headers=constants.REQUEST_HEADERS_DEFAULT,
                             auth=(self.userid, self.password), timeout=timeout)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            log.warning("an error occurred while updating IP at '%s'",
                        self.updateUrl(), exc_info=exc)
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
