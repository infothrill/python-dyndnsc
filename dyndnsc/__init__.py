# -*- coding: utf-8 -*-

import time
import logging


from . import detector
from . import updater


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

LOG = logging.getLogger(__name__)


class DynDnsClient(object):
    """This class represents a client to the dynamic dns service."""
    def __init__(self, sleeptime=300):
        self.ipchangedetection_sleep = sleeptime  # check every n seconds if our IP changed
        self.forceipchangedetection_sleep = sleeptime * 5  # force check every n seconds if our IP changed
        self.lastcheck = None
        self.lastforce = None
        self.proto = None
        self.dns = None
        self.detector = None
        self.status = 0
        LOG.debug("DynDnsClient instantiated")
        # log.growl("Network", "Dynamic DNS client activated")

    def setProtocolHandler(self, proto):
        self.proto = proto

    def setDNSDetector(self, detector):
        self.dns = detector

    def setChangeDetector(self, detector):
        self.detector = detector

    def sync(self):
        """Forces a synchronization if there is a difference between the IP from
        DNS and the detector. This can be expensive, mostly depending on the
        detector, but also because updating the dynamic ip in itself is costly.
        Therefore, this method should usually only be called on startup or when
        the state changes.
        """
        if self.dns.detect() != self.detector.detect():
            current_ip = self.detector.getCurrentValue()
            if not current_ip is None:
                LOG.info("Current dns IP '%s' does not match current detected IP '%s', updating", self.dns.getCurrentValue(), current_ip)
                self.proto.update(current_ip)
                self.status = self.proto.status
            else:
                # print self.detector.detect()
                LOG.debug("DNS is out of sync, but we don't know what to update it to (detector returns None)")
                self.status = 2
                # we don't have a value to set it to, so don't update! Still shouldn't happen though
        else:
            self.status = 0
            LOG.debug("Nothing to do, dns '%s' equals detection '%s'", self.detector.getCurrentValue(), self.detector.getCurrentValue())

    def stateHasChanged(self):
        """Detects a change either in the offline detector or a
        difference between the real DNS value and what the online
        detector last got.
        This is efficient, as it only generates minimal dns traffic
        for online detectors and no traffic at all for offline detectors.

        @return: boolean
        """
        self.lastcheck = time.time()
        # prefer offline state change detection:
        if self.detector.canDetectOffline():
            self.detector.detect()
        elif not self.dns.detect() == self.detector.getCurrentValue():  # query current dns, and only detect if there's no match
            # this produces traffic, but probably less traffic overall than the detector
            self.detector.detect()
        if self.detector.hasChanged() == True:
            LOG.debug("detector changed")
            return True
        elif self.dns.hasChanged() == True:
            LOG.debug("dns changed")
            return True
        else:
            return False

    def needsCheck(self):
        """This checks if the planned time between checks has elapsed.
        When this time has elapsed, a state change check through stateHasChanged() should be performed and eventually a sync().
        """
        if self.lastcheck is None:
            return True
        else:
            if (time.time() - self.lastcheck < self.ipchangedetection_sleep):
                return False
            else:
                return True

    def needsForcedCheck(self):
        """This checks if self.forceipchangedetection_sleep between checks has elapsed.
        When this time has elapsed, a sync() should be performed, no matter what stateHasChanged() says.
        This is really just a safety thing to enforce consistency in case the state gets messed up.
        """
        if self.lastforce is None:
            self.lastforce = time.time()
        elapsed = time.time() - self.lastforce
        if (elapsed < self.forceipchangedetection_sleep):
            return False
        return True

    def check(self):
        if self.needsCheck():
            LOG.debug("needs a check according to ipchangedetection_sleep (%s sec)", self.ipchangedetection_sleep)
            if self.stateHasChanged():
                LOG.debug("state changed, syncing...")
                self.sync()
            elif self.needsForcedCheck():
                LOG.debug("forcing sync after %s seconds", self.forceipchangedetection_sleep)
                self.lastforce = time.time()
                self.sync()
            else:
                # nothing to be done
                pass

    def loop(self):
        """Blocking endless loop with built-in sleeping between checks and updates."""
        while True:
            self.check()
            time.sleep(self.ipchangedetection_sleep)


def getDynDnsClientForConfig(config):
    """Factory method to instantiate and initialize a complete and working dyndns client

    @param config: a dictionary with configuration pairs
    """
    if config is None:
        return None
    if not 'hostname' in config:
        LOG.warn("No hostname configured")
        return None
    dnsChecker = detector.IPDetector_DNS(config['hostname'])
    try:
        klass = updater.getUpdaterClass(config['protocol'])
    except KeyError:
        LOG.warn("Invalid protocol: '%s'", config['protocol'])
        return None
    try:
        protoHandler = klass(config)
    except (AssertionError, KeyError) as e:
        LOG.warn("Invalid protocol configuration: '%s'", str(e), exc_info=e)
        return None

    dyndnsclient = DynDnsClient(sleeptime=config['sleeptime'])
    dyndnsclient.setProtocolHandler(protoHandler)
    dyndnsclient.setDNSDetector(dnsChecker)

    # allow config['method'] to be a list or a comma-separated string:
    if type([]) != type(config['method']):
        dummy = config['method'].split(',')
    else:
        dummy = config['method']
    method = dummy[0]
    if len(dummy) > 1:
        method_optlist = dummy[1:]
    else:
        method_optlist = []
    try:
        klass = detector.getDetectorClass(method)
    except (KeyError) as e:
        LOG.warn("Invalid change detector configuration: '%s'", method, exc_info=e)
        return None

    # make a dictionary from method_optlist:
    opts = {}
    colon = ":"
    for opt in method_optlist:
        # options are key value pairs, separated by a colon ":"
        # allow white-spaces in input, but strip them here:
        option, dummysep, value = opt.partition(colon)
        option = option.strip()
        if option in opts:
            LOG.warn("Option '%s' specified more than once, using '%s'.", option, value)
        opts[option] = value.strip()
    try:
        dyndnsclient.setChangeDetector(klass(opts))
    except KeyError as e:
        LOG.warn("Invalid change detector parameters: '%s'", opts, exc_info=e)
        return None

    return dyndnsclient
