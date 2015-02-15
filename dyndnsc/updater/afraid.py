# -*- coding: utf-8 -*-

"""
Basic dyndns functionality for interacting with a service compatible to
http://freedns.afraid.org/.
"""

import logging
import hashlib
import re
from collections import namedtuple

import requests

from .base import UpdateProtocol
from ..common.six import ipaddress
from ..common import constants

log = logging.getLogger(__name__)

# define a namedtuple for the records returned by the service
AfraidDynDNSRecord = namedtuple(
    'AfraidDynDNSRecord', 'hostname, ip, update_url')


class AfraidCredentials(object):

    """
    Minimal container for userid, password and sha, which will be lazily
    computed, if not provided at initialization.
    """

    def __init__(self, userid, password, sha=None):
        self._userid = userid
        self._password = password
        self._sha = sha

    @property
    def userid(self):
        return self._userid

    @property
    def password(self):
        return self._password

    @property
    def sha(self):
        if self._sha is None:
            self._sha = compute_auth_key(self.userid, self.password)
        return self._sha


def compute_auth_key(userid, password):
    """
    authentication key for freedns.afraid.org, which is the SHA1 hash of the
    string b'userid|password'

    :param userid: ascii username
    :param password: ascii password
    :return: ascii authentication key (SHA1 at this point)
    """
    import sys
    if sys.version_info >= (3, 0):
        return hashlib.sha1(b'|'.join((userid.encode('ascii'),
                                       password.encode('ascii')))).hexdigest()
    else:
        return hashlib.sha1('|'.join((userid, password))).hexdigest()


def records(credentials, url='http://freedns.afraid.org/api/'):
    """
    Yields the dynamic DNS records associated with this account

    :param credentials: an AfraidCredentials instance
    :param url: the service URL
    """
    params = dict(action='getdyndns', sha=credentials.sha)
    req = requests.get(
        url, params=params, headers=constants.REQUEST_HEADERS_DEFAULT, timeout=60)
    for record_line in (line.strip() for line in req.text.splitlines()
                        if len(line.strip()) > 0):
        yield AfraidDynDNSRecord(*record_line.split('|'))


def update(url):
    """
    Updates remote DNS record by requesting its special endpoint URL. This
    automatically picks the IP address using the HTTP connection: it is not
    possible to specify the IP address explicitly.

    :param url: URL to retrieve for triggering the update
    :return: IP address
    """
    req = requests.get(
        url, headers=constants.REQUEST_HEADERS_DEFAULT, timeout=60)
    req.close()
    # Response must contain an IP address, or else we can't parse it.
    # Also, the IP address in the response is the newly assigned IP address.
    ipregex = re.compile(r'\b(?P<ip>(?:[0-9]{1,3}\.){3}[0-9]{1,3})\b')
    ipmatch = ipregex.search(req.text)
    if ipmatch:
        return str(ipaddress(ipmatch.group('ip')))
    else:
        log.error("couldn't parse the server's response '%s'", req.text)
        return None


class UpdateProtocolAfraid(UpdateProtocol):

    """Protocol handler for http://freedns.afraid.org"""

    def __init__(self, hostname, userid, password, url="http://freedns.afraid.org/api/", **kwargs):
        self.hostname = hostname
        self._credentials = AfraidCredentials(userid, password)
        self._url = url

        super(UpdateProtocolAfraid, self).__init__()

    @staticmethod
    def configuration_key():
        return "afraid"

    def update(self, *args, **kwargs):
        return self.protocol()

    def protocol(self):
        # first find the update_url for the provided account + hostname:
        update_url = next((r.update_url for r in
                           records(self._credentials, self._url)
                           if r.hostname == self.hostname), None)
        if update_url is None:
            log.warning("Could not find hostname '%s' at '%s'",
                        self.hostname, self._url)
            return None
        else:
            return update(update_url)
