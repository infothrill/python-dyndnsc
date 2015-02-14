# -*- coding: utf-8 -*-

import logging
import re

import requests

from .base import IPDetector, AF_INET, AF_INET6, AF_UNSPEC
from ..common.six import ipaddress
from ..common import constants

log = logging.getLogger(__name__)


def _get_ip_from_url(url, parser, timeout=10):
    log.debug("Querying IP address from '%s'", url)
    try:
        r = requests.get(url, headers=constants.REQUEST_HEADERS_DEFAULT, timeout=timeout)
    except requests.exceptions.RequestException as exc:
        log.debug("webcheck failed for url '%s'", url, exc_info=exc)
        return None
    else:
        if r.status_code == 200:
            return parser(r.text)
        else:
            log.debug("Wrong http status code for '%s': %i", url, r.status_code)
    return None


def _parser_plain(text):
    try:
        return str(ipaddress(text.strip()))
    except ValueError as exc:
        log.warning("Error parsing IP address '%s'", text, exc_info=exc)
        return None


def _parser_line_regex(text, pattern="Current IP Address: (.*?)(<.*){0,1}$"):
    regex = re.compile(pattern)
    for line in text.splitlines():
        matchObj = regex.search(line)
        if matchObj is not None:
            return str(ipaddress(matchObj.group(1)))
    log.debug("Output '%s' could not be parsed", text)
    return None


def _parser_checkip_dns_he_net(text):
    return _parser_line_regex(text, pattern="Your IP address is : (.*?)(<.*){0,1}$")


def _parser_checkip(text):
    return _parser_line_regex(text, pattern="Current IP Address: (.*?)(<.*){0,1}$")


def _parser_freedns_afraid(text):
    return _parser_line_regex(text, pattern="Detected IP : (.*?)(<.*){0,1}$")


def _parser_jsonip(text):
    """Parse response text like the one returned by http://jsonip.com/."""
    import json
    try:
        return str(json.loads(text).get("ip"))
    except ValueError as exc:
        log.debug("Text '%s' could not be parsed", exc_info=exc)
        return None


class IPDetectorWebCheckBase(IPDetector):

    """Base Class for misc. web service based IP detection classes."""

    urls = None  # override in child class

    def __init__(self, url=None, parser=None, *args, **kwargs):
        """
        Initializer.

        :param url: URL to fetch and parse for IP detection
        :param parser: parser to use for above URL
        """
        super(IPDetectorWebCheckBase, self).__init__(*args, **kwargs)

        self.opts_url = url
        self.opts_parser = parser

    def can_detect_offline(self):
        """Return false, as this detector generates http traffic."""
        return False

    def detect(self):
        """
        Try to contact a remote webservice and parse the returned output.

        Determine the IP address from the parsed output and return.
        """
        if self.opts_url and self.opts_parser:
            url = self.opts_url
            parser = self.opts_parser
        else:
            from random import choice
            url, parser = choice(self.urls)
        parser = globals().get('_parser_' + parser)
        theip = _get_ip_from_url(url, parser)
        if theip is None:
            log.info("Could not detect IP using webcheck! Offline?")
        self.set_current_value(theip)
        return theip


class IPDetectorWebCheck(IPDetectorWebCheckBase):

    """
    Class to detect an IPv4 address as seen by an online web site.

    Return parsable output containing the IP address.

    Note: this detection mechanism requires ipv4 connectivity, otherwise it
          will simply not detect the IP address.
    """

    # the lack of TLS is baffling ;-(
    urls = (
        ("http://checkip.eurodyndns.org/", 'checkip'),
        ("http://dynamic.zoneedit.com/checkip.html", 'plain'),
        ("http://ipcheck.rehbein.net/", 'checkip'),
        ("http://ip.dnsexit.com/", 'plain'),
        ("http://freedns.afraid.org:8080/dynamic/check.php", 'freedns_afraid'),
        ("http://ipv4.icanhazip.com/", 'plain'),
        # ("http://ip.arix.com/", 'plain'), # stopped working
        ("http://ipv4.nsupdate.info/myip", 'plain'),
        ("http://jsonip.com/", 'jsonip'),
        ("http://checkip.dns.he.net/", 'checkip_dns_he_net'),
        ("http://ip1.dynupdate.no-ip.com/", "plain"),
        ("http://ip2.dynupdate.no-ip.com/", "plain"),
    )

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(IPDetectorWebCheck, self).__init__(*args, **kwargs)

        self.opts_family = AF_INET

    @staticmethod
    def names():
        return ("webcheck", "webcheck4")


class IPDetectorWebCheck6(IPDetectorWebCheckBase):

    """
    Class to detect an IPv6 address as seen by an online web site.

    Return parsable output containing the IP address.

    Note: this detection mechanism requires ipv6 connectivity, otherwise it
          will simply not detect the IP address.
    """

    urls = (
        ("http://ipv6.icanhazip.com/", 'plain'),
        ("http://ipv6.nsupdate.info/myip", 'plain'),
    )

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(IPDetectorWebCheck6, self).__init__(*args, **kwargs)

        self.opts_family = AF_INET6

    @staticmethod
    def names():
        return ("webcheck6", )


class IPDetectorWebCheck46(IPDetectorWebCheckBase):

    """
    Class to variably detect either an IPv4 xor IPv6 address.

    (as seen by an online web site).

    Returns parsable output containing the IP address.

    Note: this detection mechanism works with both ipv4 as well as ipv6
          connectivity, however it should be noted that most dns resolvers
          implement negative caching:

        Alternating a DNS hostname between A and AAAA records is less efficient
        than staying within the same RR-Type. This is due to the fact that most
        libc-implementations do both lookups when gettaddrinf() is called and
        therefore negative caching occurs (e.g. caching that a record does not
        exist).

        This also means that alternating only works well if the zone's SOA
        record has a minimum TTL close to the record TTL, which in turn means
        that using alternation should only be done in a dedicated (sub)domain
        with its own SOA record and a low TTL.
    """

    urls = (
        ("http://icanhazip.com/", 'plain'),
        ("http://nsupdate.info/myip", 'plain'),
    )

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(IPDetectorWebCheck46, self).__init__(*args, **kwargs)

        self.opts_family = AF_UNSPEC

    @staticmethod
    def names():
        return ("webcheck46", "webcheck64")
