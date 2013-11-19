# -*- coding: utf-8 -*-

import logging
import hashlib
import re

import requests

from ..common.subject import Subject

log = logging.getLogger(__name__)


class AfraidCredentials(object):
    '''
    Container for userid, password and sha
    '''
    def __init__(self, userid, password, sha=None):
        self._userid = userid
        self._password = password

        if sha is None:
            self._sha = compute_auth_key(self._userid, self._password)
        else:
            self._sha = sha

    @property
    def userid(self):
        return self._userid

    @property
    def password(self):
        return self._password

    @property
    def sha(self):
        return self._sha


def compute_auth_key(userid, password):
    """
    authentication key for freedns.afraid.org, which is the SHA1 hash of the
    string 'userid|password'
    """
    return hashlib.sha1('|'.join((userid, password))).hexdigest()


def get_dyndns_records(credentials, url='http://freedns.afraid.org/api/'):
    """Gets the set of dynamic DNS records associated with this account"""
    params = dict(action='getdyndns', sha=credentials.sha)
    r = requests.get(
                     url,
                     params=params,
                     timeout=60
                     )

    records = []
    #log.debug(r.text)
    for record_line in [line.strip() for line in r.text.splitlines() if len(line.strip()) > 0]:
        #log.debug("line : %s", record_line)
        hostname, ip, update_url = record_line.split('|')
        records.append({
                        'hostname': hostname,
                        'ip': ip,
                        'update_url': update_url
                        })

    return records


def update(record):
    """
    Updates remote DNS record by requesting its special endpoint URL
    """
    ip_pattern = re.compile(r'[0-9]+(?:\.[0-9]+){3}')
    r = requests.get(record['update_url'], timeout=60)
    match = ip_pattern.search(r.text)
    # response must contain an ip address, or else we can't parse it
    if not match:
        raise Exception("Couldn't parse the server's response",
                r.text)

    record['ip'] = match.group(0)
    return record['ip']


class UpdateProtocolAfraid(Subject):
    """Protocol handler for http://freedns.afraid.org"""

    _url = 'http://freedns.afraid.org/api/'

    def __init__(self, options):
        self.theip = None
        self.hostname = options['hostname']
        self._credentials = AfraidCredentials(
                                              options['userid'],
                                              options['password']
                                              )
        if 'url' in options:
            self._url = options['url']

        super(UpdateProtocolAfraid, self).__init__()

    @staticmethod
    def configuration_key():
        return "afraid"

    def update(self, ip=None):
        self.theip = ip
        return self.protocol()

    def protocol(self):
        for record in get_dyndns_records(self._credentials, self._url):
            log.debug(record)
