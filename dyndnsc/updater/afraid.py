# -*- coding: utf-8 -*-

"""Functionality for interacting with a service compatible with https://freedns.afraid.org/."""

import logging
import hashlib
import re
from collections import namedtuple

import requests

from .base import UpdateProtocol
from ..common.six import ipaddress
from ..common import constants

LOG = logging.getLogger(__name__)

# define a namedtuple for the records returned by the service
AfraidDynDNSRecord = namedtuple(
    "AfraidDynDNSRecord", "hostname, ip, update_url")


class AfraidCredentials(object):
    """
    Minimal container for credentials (userid, password).

    Computes sha checksum lazily if not provided at initialization.
    """

    def __init__(self, userid, password, sha=None):
        """
        Initialize.

        :param userid: string user id
        :param password: string password
        :param sha: optional sha checksum
        """
        self._userid = userid
        self._password = password
        self._sha = sha

    @property
    def userid(self):
        """Return userid."""
        return self._userid

    @property
    def password(self):
        """Return password."""
        return self._password

    @property
    def sha(self):
        """Return sha, lazily compute if not done yet."""
        if self._sha is None:
            self._sha = compute_auth_key(self.userid, self.password)
        return self._sha


def compute_auth_key(userid, password):
    """
    Compute the authentication key for freedns.afraid.org.

    This is the SHA1 hash of the string b'userid|password'.

    :param userid: ascii username
    :param password: ascii password
    :return: ascii authentication key (SHA1 at this point)
    """
    import sys
    if sys.version_info >= (3, 0):
        return hashlib.sha1(b"|".join((userid.encode("ascii"),  # noqa: S303
                                       password.encode("ascii")))).hexdigest()
    return hashlib.sha1("|".join((userid, password))).hexdigest()  # noqa: S303


def records(credentials, url="https://freedns.afraid.org/api/"):
    """
    Yield the dynamic DNS records associated with this account.

    :param credentials: an AfraidCredentials instance
    :param url: the service URL
    """
    params = {"action": "getdyndns", "sha": credentials.sha}
    req = requests.get(
        url, params=params, headers=constants.REQUEST_HEADERS_DEFAULT, timeout=60)
    for record_line in (line.strip() for line in req.text.splitlines()
                        if len(line.strip()) > 0):
        yield AfraidDynDNSRecord(*record_line.split("|"))


def update(url):
    """
    Update remote DNS record by requesting its special endpoint URL.

    This automatically picks the IP address using the HTTP connection: it is not
    possible to specify the IP address explicitly.

    :param url: URL to retrieve for triggering the update
    :return: IP address
    """
    req = requests.get(
        url, headers=constants.REQUEST_HEADERS_DEFAULT, timeout=60)
    req.close()
    # Response must contain an IP address, or else we can't parse it.
    # Also, the IP address in the response is the newly assigned IP address.
    ipregex = re.compile(r"\b(?P<ip>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\b")
    ipmatch = ipregex.search(req.text)
    if ipmatch:
        return str(ipaddress(ipmatch.group("ip")))
    LOG.error("couldn't parse the server's response '%s'", req.text)
    return None


class UpdateProtocolAfraid(UpdateProtocol):
    """Protocol handler for http://freedns.afraid.org ."""

    configuration_key = "afraid"

    def __init__(self, hostname, userid, password, url="https://freedns.afraid.org/api/", **kwargs):
        """
        Initialize.

        :param hostname: string hostname
        :param userid: string user id
        :param password: string password
        :param url: option API endpoint URL
        """
        self.hostname = hostname
        self._credentials = AfraidCredentials(userid, password)
        self._url = url

        super(UpdateProtocolAfraid, self).__init__()

    def update(self, *args, **kwargs):
        """Update the IP on the remote service."""
        # first find the update_url for the provided account + hostname:
        update_url = next((r.update_url for r in
                           records(self._credentials, self._url)
                           if r.hostname == self.hostname), None)
        if update_url is None:
            LOG.warning("Could not find hostname '%s' at '%s'",
                        self.hostname, self._url)
            return None
        return update(update_url)
