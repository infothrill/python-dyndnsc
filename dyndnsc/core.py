# -*- coding: utf-8 -*-

"""Module containing dyndnsc core logic."""

import logging
from logging import NullHandler
import time


from .plugins.manager import NullPluginManager
from .updater.base import UpdateProtocol
from .updater.manager import get_updater_class
from .detector.dns import IPDetector_DNS
from .detector.null import IPDetector_Null
from .detector.base import IPDetector
from .detector.manager import get_detector_class


# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())

LOG = logging.getLogger(__name__)


class DynDnsClient(object):
    """This class represents a client to the dynamic dns service."""

    def __init__(self, updater=None, detector=None, plugins=None, detect_interval=300):
        """
        Initializer.

        :param detect_interval: amount of time in seconds that can elapse between checks
        """
        if updater is None:
            raise ValueError("No updater specified")
        elif not isinstance(updater, UpdateProtocol):
            raise ValueError("updater '%r' is not an instance of '%r'" % (updater, UpdateProtocol))
        else:
            self.updater = updater
        if detector is None:
            LOG.warning("No IP detector specified, falling back to null detector.")
            self.detector = IPDetector_Null()
        elif not isinstance(detector, IPDetector):
            raise ValueError("detector '%r' is not an instance of '%r'" % (detector, IPDetector))
        else:
            self.detector = detector
        LOG.debug("IP detector uses address family %r", self.detector.af())
        if plugins is None:
            self.plugins = NullPluginManager()
        else:
            self.plugins = plugins
        hostname = self.updater.hostname  # this is kind of a kludge
        self.dns = IPDetector_DNS(hostname=hostname, family=self.detector.af())
        self.ipchangedetection_sleep = int(detect_interval)  # check every n seconds if our IP changed
        self.forceipchangedetection_sleep = int(detect_interval) * 5  # force check every n seconds if our IP changed
        self.lastcheck = None
        self.lastforce = None
        self.status = 0
        LOG.debug("DynDnsClient initializer done")

    def sync(self):
        """
        Synchronize the registered IP with the detected IP (if needed).

        This can be expensive, mostly depending on the detector, but also
        because updating the dynamic ip in itself is costly. Therefore, this
        method should usually only be called on startup or when the state changes.
        """
        detected_ip = self.detector.detect()
        if detected_ip is None:
            LOG.debug("Couldn't detect the current IP using detector %r", self.detector.names()[-1])
            # we don't have a value to set it to, so don't update! Still shouldn't happen though
        elif self.dns.detect() != detected_ip:
            LOG.info("%s: dns IP '%s' does not match detected IP '%s', updating",
                     self.updater.hostname, self.dns.get_current_value(), detected_ip)
            self.status = self.updater.update(detected_ip)
            self.plugins.after_remote_ip_update(detected_ip, self.status)
        else:
            self.status = 0
            LOG.debug("%s: nothing to do, dns '%s' equals detection '%s'",
                      self.updater.hostname,
                      self.dns.get_current_value(),
                      self.detector.get_current_value())

    def has_state_changed(self):
        """
        Detect changes in offline detector and real DNS value.

        Detect a change either in the offline detector or a
        difference between the real DNS value and what the online
        detector last got.
        This is efficient, since it only generates minimal dns traffic
        for online detectors and no traffic at all for offline detectors.

        :rtype: boolean
        """
        self.lastcheck = time.time()
        # prefer offline state change detection:
        if self.detector.can_detect_offline():
            self.detector.detect()
        elif not self.dns.detect() == self.detector.get_current_value():
            # The following produces traffic, but probably less traffic
            # overall than the detector
            self.detector.detect()

        if self.detector.has_changed():
            LOG.debug("detector changed")
            return True
        elif self.dns.has_changed():
            LOG.debug("dns changed")
            return True

        return False

    def needs_check(self):
        """
        Check if enough time has elapsed to perform a check().

        If this time has elapsed, a state change check through
        has_state_changed() should be performed and eventually a sync().

        :rtype: boolean
        """
        if self.lastcheck is None:
            return True
        return time.time() - self.lastcheck >= self.ipchangedetection_sleep

    def needs_sync(self):
        """
        Check if enough time has elapsed to perform a sync().

        A call to sync() should be performed every now and then, no matter what
        has_state_changed() says. This is really just a safety thing to enforce
        consistency in case the state gets messed up.

        :rtype: boolean
        """
        if self.lastforce is None:
            self.lastforce = time.time()
        return time.time() - self.lastforce >= self.forceipchangedetection_sleep

    def check(self):
        """
        Check if the detector changed and call sync() accordingly.

        If the sleep time has elapsed, this method will see if the attached
        detector has had a state change and call sync() accordingly.
        """
        if self.needs_check():
            if self.has_state_changed():
                LOG.debug("state changed, syncing...")
                self.sync()
            elif self.needs_sync():
                LOG.debug("forcing sync after %s seconds",
                          self.forceipchangedetection_sleep)
                self.lastforce = time.time()
                self.sync()
            else:
                # nothing to be done
                pass


def getDynDnsClientForConfig(config, plugins=None):
    """Instantiate and return a complete and working dyndns client.

    :param config: a dictionary with configuration keys
    :param plugins: an object that implements PluginManager
    """
    initparams = {}
    if "interval" in config:
        initparams["detect_interval"] = config["interval"]

    if plugins is not None:
        initparams["plugins"] = plugins

    if "updater" in config:
        for updater_name, updater_options in config["updater"]:
            initparams["updater"] = get_updater_class(updater_name)(**updater_options)

    # find class and instantiate the detector:
    if "detector" in config:
        detector_name, detector_opts = config["detector"][-1]
        try:
            klass = get_detector_class(detector_name)
        except KeyError as exc:
            LOG.warning("Invalid change detector configuration: '%s'",
                        detector_name, exc_info=exc)
            return None
        thedetector = klass(**detector_opts)
        initparams["detector"] = thedetector

    return DynDnsClient(**initparams)
