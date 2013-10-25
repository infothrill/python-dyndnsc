# -*- coding: utf-8 -*-

import logging
import socket
import random
import re

import IPy
import netifaces
import requests

from ..common.subject import Subject

LOG = logging.getLogger(__name__)


class BaseClass(Subject):
    """A common base class providing logging and desktop-notification.
    """
    def __init__(self, *args, **kwargs):
        super(BaseClass, self).__init__()
        #from dyndnsc.notifier.macgrowl import notify
        #self.register_observer(notify)

    def emit(self, message):
        """
        sends message to the notifier
        """
        self.notify_observers(event='Dynamic DNS', msg=message)


class IPDetector(BaseClass):
    """
    Base class for IP detectors. Really is just a state machine for
    old/current value.
    """
    def __init__(self, *args, **kwargs):
        super(IPDetector, self).__init__()

    def canDetectOffline(self):
        """
        Must be overwritten. Return True when the IP detection can work
        offline without causing network traffic.
        """
        raise NotImplementedError("Abstract method, must be overridden")

    def getOldValue(self):
        if not '_oldvalue' in vars(self):
            self._oldvalue = self.getCurrentValue()
        return self._oldvalue

    def setOldValue(self, value):
        self._oldvalue = value

    def getCurrentValue(self, default=None):
        if not hasattr(self, '_currentvalue'):
            self._currentvalue = default
        return self._currentvalue

    def setCurrentValue(self, value):
        if value != self.getCurrentValue(value):
            self._oldvalue = self.getCurrentValue(value)
            self._currentvalue = value
            self.emit("new IP detected: %s" % str(value))
        return value

    def hasChanged(self):
        """Detect a state change with old and current value"""
        if self.getOldValue() == self.getCurrentValue():
            return False
        else:
            return True


class IPDetector_DNS(IPDetector):
    """Class to resolve a hostname using socket.getaddrinfo()"""
    def __init__(self, hostname):
        self._hostname = hostname
        super(IPDetector_DNS, self).__init__()

    @staticmethod
    def getName():
        return "dns"

    def canDetectOffline(self):
        """Returns false, as this detector generates dns traffic"""
        return False

    def detect(self):
        try:
            theip = socket.getaddrinfo(self._hostname, None)[0][4][0]
        except:
            # logging.debug("WARN: dns is None")
            theip = None
        # logging.debug("dnsdetect for %s: %s", self.hostname, ip)
        self.setCurrentValue(theip)
        return theip


class IPDetector_Command(IPDetector):
    """IPDetector to detect IP adress executing shell command/script"""
    def __init__(self, options):
        """
        Constructor
        @param options: dictionary

        available options:

        command: shell command that writes IP address to STDOUT
        """
        self.opts = {'command': ''}
        for k in options.keys():
            LOG.debug("%s explicitly got option: %s -> %s", self.__class__.__name__, k, options[k])
            self.opts[k] = options[k]
        super(IPDetector_Command, self).__init__()

    @staticmethod
    def getName():
        return "command"

    def canDetectOffline(self):
        """Returns false, as this detector possibly generates network traffic"""
        return False

    def setHostname(self, hostname):
        self.hostname = hostname

    def detect(self):
        import sys
        if sys.version_info >= (3, 0):
            import subprocess
        else:
            import commands as subprocess
        try:
            theip = subprocess.getoutput(self.opts['command'])
        except:
            theip = None
        self.setCurrentValue(theip)
        return theip


class RandomIPGenerator(object):
    def __init__(self, maxRandomTries=None):
        self.maxRandomTries = maxRandomTries

        # Reserved list from http://www.iana.org/assignments/ipv4-address-space
        # (dated  2010-02-22)
        self._reserved_netmasks = frozenset([
                "0.0.0.0/8",
                "5.0.0.0/8",
                "10.0.0.0/8",
                "23.0.0.0/8",
                "31.0.0.0/8",
                "36.0.0.0/8",
                "39.0.0.0/8",
                "42.0.0.0/8",
                "127.0.0.0/8",
                "169.254.0.0/16",
                "172.16.0.0/12",
                "192.168.0.0/16",
                "224.0.0.0/3",
                "240.0.0.0/8"
                ])

    def isReservedIP(self, ip):
        """Check if the given ip address is in a reserved ipv4 address space

        @param ip: IPy ip address
        @return: boolean
        """
        for res in self._reserved_netmasks:
            if ip in IPy.IP(res):
                return True
        return False

    def randomIP(self):
        """Return a randomly generated IPv4 address that is not in a reserved ipv4 address space

        @return: IPy ip address
        """
        randomip = IPy.IP("%i.%i.%i.%i" % (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)))
        while self.isReservedIP(randomip):
            randomip = IPy.IP("%i.%i.%i.%i" % (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)))
        return randomip

    def next(self):
        return self.__next__()

    def __next__(self):
        """Generator that returns randomly generated IPv4 addresses that are not in a reserved ipv4 address space
        until we hit self.maxRandomTries

        @return: IPy ip address
        """
        if self.maxRandomTries is None or self.maxRandomTries > 0:
            generate = True
        c = 0
        while generate:
            if not self.maxRandomTries is None:
                c += 1
            yield self.randomIP()
            if not self.maxRandomTries is None and c < self.maxRandomTries:
                generate = False

        raise StopIteration

    def __iter__(self):
        """Iterator for this class. See method next()"""
        return next(self)


class IPDetector_Random(IPDetector):
    """For testing: detect randomly generated IP addresses"""
    def __init__(self, options):
        super(IPDetector_Random, self).__init__()
        self.rips = RandomIPGenerator()

    @staticmethod
    def getName():
        return "random"

    def canDetectOffline(self):
        """Returns True"""
        return True

    def detect(self):
        for theip in self.rips:
            LOG.debug('detected %s', str(theip))
            self.setCurrentValue(str(theip))
            return str(theip)


class IPDetector_Iface(IPDetector):
    """IPDetector to detect any ip address of a local interface.
    """
    def __init__(self, options=None):
        """
        Constructor
        @param options: dictionary

        available options:

        iface: name of interface (default: en0)
        family: IP address family (default: INET, possible: INET6)
        netmask: netmask to be matched if multiple IPs on interface (default: none (match all)", example for teredo: "2001:0000::/32")
        """
        if options is None:
            options = {}
        self.opts = {'iface': 'en0', 'family': "INET", "netmask": None}
        for k in options.keys():
            LOG.debug("%s explicitly got option: %s -> %s", self.__class__.__name__, k, options[k])
            self.opts[k] = options[k]
        super(IPDetector_Iface, self).__init__()

    @staticmethod
    def getName():
        return "iface"

    def canDetectOffline(self):
        """Returns true, as this detector only queries local data"""
        return True

    def _detect(self):
        """uses the netifaces module to detect ifconfig information"""
        if (not 'netmask' in vars(self)):
            if (not self.opts['netmask'] is None):  # if a netmask was given
                try:
                    self.netmask = IPy.IP(self.opts['netmask'])
                except (TypeError, ValueError) as e:
                    # TODO: this is a potential trust issue, because if we don't
                    # fail here, we might end up sending an IP to the outside
                    # world that should be hidden (because in a "private" netmask)
                    LOG.error("Choked while parsing netmask '%s'", self.opts["netmask"], exc_info=e)
                    self.netmask = None

            else:
                self.netmask = None
        theip = None
        try:
            if self.opts['family'] == 'INET6':
                addrlist = netifaces.ifaddresses(self.opts['iface'])[netifaces.AF_INET6]
            else:
                addrlist = netifaces.ifaddresses(self.opts['iface'])[netifaces.AF_INET]
        except Exception as e:
            LOG.error("netifaces choked while trying to get inet6 interface information for interface '%s'", self.opts['iface'], exc_info=e)
        else:  # now we have a list of addresses as returned by netifaces
            for pair in addrlist:
                try:
                    detip = IPy.IP(pair['addr'])
                except (TypeError, ValueError) as e:
                    LOG.debug("Found invalid IP '%s' on interface '%s'!?", pair['addr'], self.opts['iface'])
                    continue
                if (not self.netmask is None):
                    if (detip in self.netmask):
                        theip = pair['addr']
                    else:
                        continue
                else:
                    theip = pair['addr']
                break  # we use the first IP found
        # theip can still be None at this point!
        self.setCurrentValue(theip)
        return theip

    def detect(self):
        return self._detect()


class IPDetector_Teredo(IPDetector_Iface):
    """IPDetector to detect a Teredo ipv6 address of a local interface.
    Bits 0 to 31 of the ipv6 address are set to the Teredo prefix (normally 2001:0000::/32).
    This detector only checks the first 16 bits!
    See http://en.wikipedia.org/wiki/Teredo_tunneling for more information on Teredo.

    Inherits IPDetector_Iface and sets default options only
    """
    def __init__(self, options=None):
        """
        Constructor
        @param options: dictionary
        """
        if options is None:
            options = {}
        super(IPDetector_Teredo, self).__init__(options)
        self.opts = {'iface': 'tun0', 'family': "INET6", "netmask": "2001:0000::/32"}
        for k in options.keys():
            LOG.debug("%s explicitly got option: %s -> %s", self.__class__.__name__, k, options[k])
            self.opts[k] = options[k]

    @staticmethod
    def getName():
        return "teredo"


class IPDetector_WebCheck(IPDetector):
    """Class to detect an IP address as seen by an online web site that returns parsable output"""

    @staticmethod
    def getName():
        return "webcheck"

    def canDetectOffline(self):
        """Returns false, as this detector generates http traffic"""
        return False

    def _getClientIPFromUrl(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                regex = re.compile("Current IP Address: (.*?)(<.*){0,1}$")
                for line in r.text.splitlines():
                    matchObj = regex.search(line)
                    if not matchObj is None:
                        return str(IPy.IP(matchObj.group(1)))
        except (requests.exceptions.RequestException):
            pass
        return None

    def detect(self):
        # self.LOG("detect WebCheck")
        from random import choice
        urls = (
                "http://checkip.dyndns.org/",
                "http://checkip.eurodyndns.org/",
                "http://dynamic.zoneedit.com/checkip.html",  # renders bad stuff if queried too quickly, but that's fine ;-)
                "http://ipcheck.rehbein.net/"
                "http://www.antifart.com/stuff/checkip/",
                )
        theip = self._getClientIPFromUrl(choice(urls))
        if theip is None:
            LOG.info("Could not detect IP using webchecking! Offline?")
        self.setCurrentValue(theip)
        return theip
