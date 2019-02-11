# -*- coding: utf-8 -*-

"""Module containing logic for webcheck based detectors."""

import logging
from random import choice
import re

import requests

from .base import IPDetector, AF_INET, AF_INET6, AF_UNSPEC
from ..common.six import ipaddress
from ..common import constants

LOG = logging.getLogger(__name__)


def _get_ip_from_url(url, parser, timeout=10):
    LOG.debug("Querying IP address from '%s'", url)
    try:
        req = requests.get(url, headers=constants.REQUEST_HEADERS_DEFAULT, timeout=timeout)
    except requests.exceptions.RequestException as exc:
        LOG.debug("webcheck failed for url '%s'", url, exc_info=exc)
        return None
    else:
        if req.status_code == 200:
            return parser(req.text)
        else:
            LOG.debug("Wrong http status code for '%s': %i", url, req.status_code)
    return None


def _parser_plain(text):
    try:
        return str(ipaddress(text.strip()))
    except ValueError as exc:
        LOG.warning("Error parsing IP address '%s':", text, exc_info=exc)
        return None


def _parser_line_regex(text, pattern="Current IP Address: (.*?)(<.*){0,1}$"):
    regex = re.compile(pattern)
    for line in text.splitlines():
        match_obj = regex.search(line)
        if match_obj is not None:
            return str(ipaddress(match_obj.group(1)))
    LOG.debug("Output '%s' could not be parsed", text)
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
        LOG.debug("Text '%s' could not be parsed", exc_info=exc)
        return None


class IPDetectorWebCheckBase(IPDetector):
    """Base Class for misc. web service based IP detection classes."""

    urls = None  # override in child class
    configuration_key = None

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
            url, parser = choice(self.urls)  # noqa: S311
        parser = globals().get("_parser_" + parser)
        theip = _get_ip_from_url(url, parser)
        if theip is None:
            LOG.info("Could not detect IP using webcheck! Offline?")
        self.set_current_value(theip)
        return theip


class IPDetectorWebCheck(IPDetectorWebCheckBase):
    """
    Class to detect an IPv4 address as seen by an online web site.

    Return parsable output containing the IP address.

    .. note::
        This detection mechanism requires ipv4 connectivity, otherwise it
        will simply not detect the IP address.
    """

    configuration_key = "webcheck4"

    # TODO: consider throwing out all URLs with no TLS support
    urls = (
        ("http://checkip.eurodyndns.org/", "checkip"),
        ("http://ip.dnsexit.com/", "plain"),
        ("http://checkip.dns.he.net/", "checkip_dns_he_net"),
        ("http://ip1.dynupdate.no-ip.com/", "plain"),
        ("http://ip2.dynupdate.no-ip.com/", "plain"),
        ("https://api.ipify.org/", "plain"),
        ("https://dynamic.zoneedit.com/checkip.html", "plain"),
        ("https://freedns.afraid.org/dynamic/check.php", "freedns_afraid"),
        ("https://ifconfig.co/ip", "plain"),
        ("https://ipinfo.io/ip", "plain"),
        ("https://ipv4.icanhazip.com/", "plain"),
        ("https://ipv4.nsupdate.info/myip", "plain"),
        ("https://jsonip.com/", "jsonip"),
    )

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(IPDetectorWebCheck, self).__init__(*args, **kwargs)

        self.opts_family = AF_INET


class IPDetectorWebCheck6(IPDetectorWebCheckBase):
    """
    Class to detect an IPv6 address as seen by an online web site.

    Return parsable output containing the IP address.

    Note: this detection mechanism requires ipv6 connectivity, otherwise it
          will simply not detect the IP address.
    """

    configuration_key = "webcheck6"

    urls = (
        ("https://ipv6.icanhazip.com/", "plain"),
        ("https://ipv6.nsupdate.info/myip", "plain"),
        ("https://v6.ident.me", "plain"),
    )

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(IPDetectorWebCheck6, self).__init__(*args, **kwargs)

        self.opts_family = AF_INET6


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
        libc-implementations do both lookups when getaddrinf() is called and
        therefore negative caching occurs (e.g. caching that a record does not
        exist).

        This also means that alternating only works well if the zone's SOA
        record has a minimum TTL close to the record TTL, which in turn means
        that using alternation should only be done in a dedicated (sub)domain
        with its own SOA record and a low TTL.
    """

    configuration_key = "webcheck46"

    urls = (
        ("https://icanhazip.com/", "plain"),
        ("https://www.nsupdate.info/myip", "plain"),
        ("https://ident.me", "plain"),
    )

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super(IPDetectorWebCheck46, self).__init__(*args, **kwargs)

        self.opts_family = AF_UNSPEC
