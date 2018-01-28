# -*- coding: utf-8 -*-

"""Module providing functionality to interact with dyndns2 compatible services."""

from logging import getLogger

import requests

from .base import UpdateProtocol
from ..common import constants

LOG = getLogger(__name__)


class UpdateProtocolDyndns2(UpdateProtocol):
    """Updater for services compatible with the dyndns2 protocol."""

    configuration_key = "dyndns2"

    def __init__(self, hostname, userid, password, url, *args, **kwargs):
        """
        Initialize.

        :param hostname: the fully qualified hostname to be managed
        :param userid: the userid for identification
        :param password: the password for authentication
        :param url: the API URL for updating the DNS entry
        """
        self.hostname = hostname
        self.__userid = userid
        self.__password = password
        self._updateurl = url

        super(UpdateProtocolDyndns2, self).__init__()

    def update(self, ip):
        """Update the IP on the remote service."""
        timeout = 60
        LOG.debug("Updating '%s' to '%s' at service '%s'", self.hostname, ip, self._updateurl)
        params = {"myip": ip, "hostname": self.hostname}
        req = requests.get(self._updateurl, params=params, headers=constants.REQUEST_HEADERS_DEFAULT,
                           auth=(self.__userid, self.__password), timeout=timeout)
        LOG.debug("status %i, %s", req.status_code, req.text)
        if req.status_code == 200:
            # responses can also be "nohost", "abuse", "911", "notfqdn"
            if req.text.startswith("good ") or req.text.startswith("nochg"):
                return ip
            return req.text
        return "invalid http status code: %s" % req.status_code
