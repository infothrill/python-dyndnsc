# -*- coding: utf-8 -*-

import logging

import requests

from ..common.subject import Subject
from ..common.events import IP_UPDATE_SUCCESS, IP_UPDATE_ERROR

log = logging.getLogger(__name__)


class UpdateProtocol(Subject):
    """
    base class for all update protocols that use the dyndns2 update protocol
    """

    _updateurl = None
    theip = None
    hostname = None  # this holds the desired dns hostname

    def __init__(self):
        self.updateurl = self._updateurl
        super(UpdateProtocol, self).__init__()

    def updateUrl(self):
        return self.updateurl

    def protocol(self):
        timeout = 60
        params = {'myip': self.theip, 'hostname': self.hostname}
        try:
            r = requests.get(self.updateUrl(), params=params,
                             auth=(self.userid, self.password), timeout=timeout)
        except requests.exceptions.Timeout as exc:
            log.warning("HTTP timeout(%i) occurred while updating IP at '%s'",
                      timeout, self.updateUrl(), exc_info=exc)
            return False
        else:
            r.close()
        log.debug("status %i, %s", r.status_code, r.text)
        if r.status_code == 200:
            if r.text.startswith("good "):
                self.notify_observers(IP_UPDATE_SUCCESS,
                    "Updated IP address of '%s' to %s"
                        % (self.hostname, self.theip))
                return self.theip
            elif r.text.startswith('nochg'):
                return self.theip
            elif r.text == 'nohost':
                self.notify_observers(IP_UPDATE_ERROR,
                    "Invalid/non-existant hostname: [%s]" % (self.hostname))
                return 'nohost'
            elif r.text == 'abuse':
                self.notify_observers(IP_UPDATE_ERROR,
                    "This client is considered to be abusive for hostname '%s'"
                        % (self.hostname))
                return 'abuse'
            elif r.text == '911':
                self.notify_observers(IP_UPDATE_ERROR, "Service is failing")
                return '911'
            elif r.text == 'notfqdn':
                self.notify_observers(IP_UPDATE_ERROR,
                    "The provided hostname '%s' is not a valid hostname!"
                        % (self.hostname))
                return 'notfqdn'
            else:
                self.notify_observers(IP_UPDATE_ERROR,
                        "Problem updating IP address of '%s' to %s: %s"
                            % (self.hostname, self.theip, r.text))
                return r.text
        else:
            self.notify_observers(IP_UPDATE_ERROR,
                "Problem updating IP address of '%s' to %s: %s"
                    % (self.hostname, self.theip, r.status_code))
            return 'invalid http status code: %s' % r.status_code
