# -*- coding: utf-8 -*-

"""Module containing the logic for updating DNS records using the duckdns protocol.

From the duckdns.org website:

https://{DOMAIN}/update?domains={DOMAINLIST}&token={TOKEN}&ip={IP}

where:
    DOMAIN the service domain
    DOMAINLIST is either a single domain or a comma separated list of domains
    TOKEN is the API token for authentication/authorization
    IP is either the IP or blank for auto-detection

"""

from logging import getLogger

from .base import UpdateProtocol
from ..common import constants

import requests

log = getLogger(__name__)


class UpdateProtocolDuckdns(UpdateProtocol):

    """Updater for services compatible with the duckdns protocol."""

    def __init__(self, hostname, token, url, *args, **kwargs):
        """
        Initializer.

        :param hostname: the fully qualified hostname to be managed
        :param token: the token for authentication
        :param url: the API URL for updating the DNS entry
        """
        self.hostname = hostname
        self.token = token
        self._updateurl = url

        super(UpdateProtocolDuckdns, self).__init__()

    @staticmethod
    def configuration_key():
        """Human readable string identifying this update protocol."""
        return "duckdns"

    def update(self, ip):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        timeout = 60
        log.debug("Updating '%s' to '%s' at service '%s'", self.hostname, self.theip, self.url())
        params = {'domains': self.hostname.partition(".")[0], 'token': self.token}
        if self.theip is None:
            params['ip'] = ""
        else:
            params['ip'] = self.theip
        # log.debug("Update params: %r", params)
        try:
            r = requests.get(self.url(), params=params, headers=constants.REQUEST_HEADERS_DEFAULT,
                             timeout=timeout)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            log.warning("an error occurred while updating IP at '%s'",
                        self.url(), exc_info=exc)
            return False
        else:
            r.close()
        log.debug("status %i, %s", r.status_code, r.text)
        # TODO: duckdns response codes seem undocumented...
        if r.status_code == 200:
            if r.text.startswith("OK"):
                return self.theip
            else:
                return r.text
        else:
            return 'invalid http status code: %s' % r.status_code
