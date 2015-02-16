# -*- coding: utf-8 -*-

import time
import logging


from .plugins.manager import NullPluginManager
from .updater.manager import get_updater_class
from .detector.manager import get_detector_class


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

log = logging.getLogger(__name__)


class DynDnsClient(object):
    """This class represents a client to the dynamic dns service."""
    def __init__(self, detect_interval=300):
        """
        Initializer

        :param detect_interval: amount of time in seconds that can elapse between checks
        """
        self.ipchangedetection_sleep = int(detect_interval)  # check every n seconds if our IP changed
        self.forceipchangedetection_sleep = int(detect_interval) * 5  # force check every n seconds if our IP changed
        self.lastcheck = None
        self.lastforce = None
        self.updaters = []
        self.dns = None
        self.detector = None
        self.status = 0
        self.plugins = NullPluginManager()
        log.debug("DynDnsClient instantiated")

    def add_updater(self, updater):
        """
        Add an updater to the client

        :param updater: an instance of type `dyndnsc.updater.UpdateProtocol`
        """
        self.updaters.append(updater)

    def set_dns_detector(self, detector):
        """
        Set the DNS detector to be used for querying the DNS

        :param detector: an instance of `dyndnsc.detector.base.IPDetector`
        """
        self.dns = detector

    def set_detector(self, detector):
        """
        Set the detector to be used to detect our IP

        :param detector: an instance of `dyndnsc.detector.base.IPDetector`
        """
        self.detector = detector

    def sync(self):
        """
        Forces a synchronization to the remote service if there is a
        difference between the IP from DNS and the detector. This can be
        expensive, mostly depending on the detector, but also because updating
        the dynamic ip in itself is costly. Therefore, this method should
        usually only be called on startup or when the state changes.
        """
        if self.dns.detect() != self.detector.detect():
            detected_ip = self.detector.get_current_value()
            if detected_ip is None:
                log.debug("DNS out of sync, but detector returned None")
                self.status = 2
                # we don't have a value to set it to, so don't update! Still shouldn't happen though
            else:
                log.info("Current dns IP '%s' does not match detected IP '%s', updating",
                         self.dns.get_current_value(), detected_ip)
                # TODO: perform some kind of proxy chaining here?
                for ipupdater in self.updaters:
                    status = ipupdater.update(detected_ip)
                self.status = status
                self.plugins.after_remote_ip_update(detected_ip, status)
        else:
            self.status = 0
            log.debug("Nothing to do, dns '%s' equals detection '%s'",
                      self.dns.get_current_value(),
                      self.detector.get_current_value())

    def has_state_changed(self):
        """
        Detects a change either in the offline detector or a
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
            log.debug("detector changed")
            return True
        elif self.dns.has_changed():
            log.debug("dns changed")
            return True
        else:
            return False

    def needs_check(self):
        """
        This checks if the planned time between checks has elapsed.
        When this time has elapsed, a state change check through
        has_state_changed() should be performed and eventually a sync().

        :rtype: boolean
        """
        if self.lastcheck is None:
            return True
        else:
            return time.time() - self.lastcheck >= self.ipchangedetection_sleep

    def needs_forced_check(self):
        """This checks if self.forceipchangedetection_sleep between checks has
        elapsed. When this time has elapsed, a sync() should be performed, no
        matter what has_state_changed() says. This is really just a safety thing
        to enforce consistency in case the state gets messed up.

        :rtype: boolean
        """
        if self.lastforce is None:
            self.lastforce = time.time()
        return time.time() - self.lastforce >= self.forceipchangedetection_sleep

    def check(self):
        """
        If the sleep time has elapsed, this method will see if the attached
        detector has had a state change and call sync() accordingly.
        """
        if self.needs_check():
            if self.has_state_changed():
                log.debug("state changed, syncing...")
                self.sync()
            elif self.needs_forced_check():
                log.debug("forcing sync after %s seconds",
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
    if 'interval' in config:
        dyndnsclient = DynDnsClient(detect_interval=config['interval'])
    else:
        dyndnsclient = DynDnsClient()

    if plugins is not None:
        log.debug("Attaching plugins to dyndnsc")
        dyndnsclient.plugins = plugins

    if 'updater' not in config:
        raise ValueError("No updater specified")
    # require at least 1 updater:
    if len(config['updater']) < 1:
        raise ValueError("At least 1 dyndns updater must be specified")
    else:
        for updater_name, updater_options in config['updater']:
            dyndnsclient.add_updater(get_updater_class(updater_name)(**updater_options))

    # find class and instantiate the detector:
    if 'detector' not in config:
        raise ValueError("No detector specified")
    detector_name, detector_opts = config['detector'][-1]
    try:
        klass = get_detector_class(detector_name)
    except KeyError as exc:
        log.warning("Invalid change detector configuration: '%s'",
                    detector_name, exc_info=exc)
        return None
    thedetector = klass(**detector_opts)
    dyndnsclient.set_detector(thedetector)

    log.debug("Doing IP detecting using address family %r", thedetector.af())

    # add the DNS detector with the same address family option as the user
    # configured detector:
    klass = get_detector_class("dns")
    dyndnsclient.set_dns_detector(klass(hostname=config['updater'][0][1]['hostname'], family=thedetector.af()))

    return dyndnsclient
