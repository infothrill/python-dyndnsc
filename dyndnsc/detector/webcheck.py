# -*- coding: utf-8 -*-

import logging
import re

import requests

from .base import IPDetector
from ..common.six import ipaddress

log = logging.getLogger(__name__)


def _get_ip_from_url(url, parser, timeout=10):
    log.debug("Querying IP address from '%s'", url)
    try:
        r = requests.get(url, timeout=timeout)
    except (requests.exceptions.RequestException) as exc:
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


def _parser_checkip(text):
    regex = re.compile("Current IP Address: (.*?)(<.*){0,1}$")
    for line in text.splitlines():
        matchObj = regex.search(line)
        if not matchObj is None:
            return str(ipaddress(matchObj.group(1)))
    log.debug("Output '%s' could not be parsed", text)
    return None


def _parser_freedns_afraid(text):
    regex = re.compile("Detected IP : (.*?)(<.*){0,1}$")
    for line in text.splitlines():
        matchObj = regex.search(line)
        if not matchObj is None:
            return str(ipaddress(matchObj.group(1)))
    log.debug("Output '%s' could not be parsed", text)
    return None


def _parser_jsonip(text):
    """Parses response text like the one returned by http://jsonip.com/"""
    import json
    try:
        return str(json.loads(text).get("ip"))
    except ValueError as exc:
        log.debug("Text '%s' could not be parsed", exc_info=exc)
        return None


class IPDetectorWebCheck(IPDetector):
    """
    Class to detect an IPv4 address as seen by an online web site that
    returns parsable output containing the IP address.

    Note: this detection mechanism requires ipv4 connectivity, otherwise it
          will simply not detect the IP address.
    """

    @staticmethod
    def names():
        return ("webcheck", "webcheck4")

    def can_detect_offline(self):
        """Returns false, as this detector generates http traffic"""
        return False

    def detect(self):
        '''
        Will try to contact a remote webservice and parse the returned output
        to determine the IP address
        '''
        from random import choice
        urls = (
                ("http://checkip.dyndns.org/", _parser_checkip),
                ("http://checkip.eurodyndns.org/", _parser_checkip),
                ("http://dynamic.zoneedit.com/checkip.html", _parser_checkip),
                ("http://ipcheck.rehbein.net/", _parser_checkip),
                ("http://ip.dnsexit.com/", _parser_plain),
                ("http://freedns.afraid.org:8080/dynamic/check.php",
                                                    _parser_freedns_afraid),
                ("http://ipv4.icanhazip.com/", _parser_plain),
                ("http://ip.arix.com/", _parser_plain),
                ("http://ipv4.nsupdate.info/myip", _parser_plain),
                ("http://jsonip.com/", _parser_jsonip),
                )
        theip = _get_ip_from_url(*choice(urls))
        if theip is None:
            log.info("Could not detect IP using webcheck! Offline?")
        self.set_current_value(theip)
        return theip


class IPDetectorWebCheck6(IPDetector):
    """
    Class to detect an IPv6 address as seen by an online web site that
    returns parsable output containing the IP address.

    Note: this detection mechanism requires ipv6 connectivity, otherwise it
          will simply not detect the IP address.
    """

    @staticmethod
    def names():
        return ("webcheck6",)

    def can_detect_offline(self):
        """Returns false, as this detector generates http traffic"""
        return False

    def detect(self):
        '''
        Will try to contact a remote webservice and parse the returned output
        to determine the IP address
        '''
        from random import choice
        # we only know few webpages that provide this...
        urls = (
                ("http://ipv6.icanhazip.com/", _parser_plain),
                ("http://ipv6.nsupdate.info/myip", _parser_plain),
                )
        theip = _get_ip_from_url(*choice(urls))
        if theip is None:
            log.info("Could not detect IP! Offline?")
        self.set_current_value(theip)
        return theip


class IPDetectorWebCheck46(IPDetector):
    """
    Class to variably detect either an IPv4 xor IPv6 address as seen by an
    online web site that returns parsable output containing the IP address.

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

    @staticmethod
    def names():
        return ("webcheck46", "webcheck64")

    def can_detect_offline(self):
        """Returns false, as this detector generates http traffic
        :return: False"""
        return False

    def detect(self):
        '''
        Will try to contact a remote webservice and parse the returned output
        to determine the IP address
        '''
        from random import choice
        # we only know few webpages that provide this...
        urls = (
                ("http://icanhazip.com/", _parser_plain),
                ("http://nsupdate.info/myip", _parser_plain),
                )
        theip = _get_ip_from_url(*choice(urls))
        if theip is None:
            log.info("Could not detect IP! Offline?")
        self.set_current_value(theip)
        return theip
