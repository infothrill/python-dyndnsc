# -*- coding: utf-8 -*-

import logging
import re

import IPy
import requests

from .base import IPDetector

log = logging.getLogger(__name__)


def _get_ip_from_url(url, parser):
    log.debug("Querying IP address from '%s'", url)
    try:
        r = requests.get(url)
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
        return str(IPy.IP(text.strip()))
    except ValueError as exc:
        log.warn("Error parsing IP address '%s'", text, exc_info=exc)
        return None


def _parser_checkip(text):
    regex = re.compile("Current IP Address: (.*?)(<.*){0,1}$")
    for line in text.splitlines():
        matchObj = regex.search(line)
        if not matchObj is None:
            return str(IPy.IP(matchObj.group(1)))
    log.debug("Output '%s' could not be parsed", text)
    return None


def _parser_freedns_afraid(text):
    regex = re.compile("Detected IP : (.*?)(<.*){0,1}$")
    for line in text.splitlines():
        matchObj = regex.search(line)
        if not matchObj is None:
            return str(IPy.IP(matchObj.group(1)))
    log.debug("Output '%s' could not be parsed", text)
    return None


class IPDetector_WebCheck(IPDetector):
    """Class to detect an IP address as seen by an online web site that returns
    parsable output containing the IP address"""

    @staticmethod
    def getName():
        return "webcheck"

    def can_detect_offline(self):
        """Returns false, as this detector generates http traffic"""
        return False

    def detect(self):
        from random import choice
        urls = (
                ("http://checkip.dyndns.org/", _parser_checkip),
                ("http://checkip.eurodyndns.org/", _parser_checkip),
                ("http://dynamic.zoneedit.com/checkip.html", _parser_checkip),
                ("http://ipcheck.rehbein.net/", _parser_checkip),
                ("http://ip.dnsexit.com/", _parser_plain),
                ("http://freedns.afraid.org:8080/dynamic/check.php", _parser_freedns_afraid),
                ("http://icanhazip.com/", _parser_plain),
                ("http://ip.arix.com/", _parser_plain),
                ("http://ipv4.nsupdate.info/myip", _parser_plain),
                )
        theip = _get_ip_from_url(*choice(urls))
        if theip is None:
            log.info("Could not detect IP using webcheck! Offline?")
        self.set_current_value(theip)
        return theip
