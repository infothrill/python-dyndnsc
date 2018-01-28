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

import requests

from .base import UpdateProtocol
from ..common import constants

LOG = getLogger(__name__)


class UpdateProtocolDuckdns(UpdateProtocol):
    """Updater for services compatible with the duckdns protocol."""

    configuration_key = "duckdns"

    def __init__(self, hostname, token, url, *args, **kwargs):
        """
        Initialize.

        :param hostname: the fully qualified hostname to be managed
        :param token: the token for authentication
        :param url: the API URL for updating the DNS entry
        """
        self.hostname = hostname
        self.__token = token
        self._updateurl = url

        super(UpdateProtocolDuckdns, self).__init__()

    def update(self, ip):
        """Update the IP on the remote service."""
        timeout = 60
        LOG.debug("Updating '%s' to '%s' at service '%s'", self.hostname, ip, self._updateurl)
        params = {"domains": self.hostname.partition(".")[0], "token": self.__token}
        if ip is None:
            params["ip"] = ""
        else:
            params["ip"] = ip
        # LOG.debug("Update params: %r", params)
        req = requests.get(self._updateurl, params=params, headers=constants.REQUEST_HEADERS_DEFAULT,
                           timeout=timeout)
        LOG.debug("status %i, %s", req.status_code, req.text)
        # duckdns response codes seem undocumented...
        if req.status_code == 200:
            if req.text.startswith("OK"):
                return ip
            return req.text
        return "invalid http status code: %s" % req.status_code
