# -*- coding: utf-8 -*-

import logging

import IPy
import netifaces

from .base import IPDetector

log = logging.getLogger(__name__)


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
        netmask: netmask to be matched if multiple IPs on interface (default:
        none (match all)", example for teredo: "2001:0000::/32")
        """
        if options is None:
            options = {}
        self.opts = {'iface': 'en0', 'family': "INET", "netmask": None}
        for k in options.keys():
            log.debug("%s explicitly got option: %s -> %s",
                      self.__class__.__name__, k, options[k])
            self.opts[k] = options[k]
        super(IPDetector_Iface, self).__init__()

    @staticmethod
    def getName():
        return "iface"

    def can_detect_offline(self):
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
                    # world that should be hidden (because in a "private"
                    # netmask)
                    log.error("Choked while parsing netmask '%s'",
                              self.opts["netmask"], exc_info=e)
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
            log.error("netifaces choked while trying to get inet6 interface"
                      " information for interface '%s'", self.opts['iface'],
                      exc_info=e)
        else:  # now we have a list of addresses as returned by netifaces
            for pair in addrlist:
                try:
                    detip = IPy.IP(pair['addr'])
                except (TypeError, ValueError) as e:
                    log.debug("Found invalid IP '%s' on interface '%s'!?",
                              pair['addr'], self.opts['iface'])
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
        self.set_current_value(theip)
        return theip

    def detect(self):
        return self._detect()
