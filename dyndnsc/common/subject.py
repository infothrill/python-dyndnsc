# -*- coding: utf-8 -*-
"""
observer/subject implementation
"""

import logging

log = logging.getLogger(__name__)


class Subject(object):
    """
    Subject -> dispatches messages to interested callables
    """
    def __init__(self):
        self._observers = {}

    def register_observer(self, observer, events=None):
        """
        register a listener function

        Parameters
        -----------
        observer : external listener function
        events  : tuple or list of relevant events (default=None)
        """
        if events is not None and type(events) not in (tuple, list):
            events = (events,)

        if observer in self._observers:
            log.warn("Observer '%r' already registered, overwriting for events"
                     " %r", observer, events)
        self._observers[observer] = events

    def notify_observers(self, event=None, msg=None):
        """notify observers """
        for observer, events in list(self._observers.items()):
            #log.debug("trying to notify the observer")
            if events is None or event is None or event in events:
                try:
                    observer(self, event, msg)
                except (Exception,) as ex:  # pylint: disable=W0703
                    self.unregister_observer(observer)
                    errmsg = "Exception in message dispatch: Handler '{0}' unregistered for event '{1}'  ".format(observer.__class__.__name__, event)
                    log.error(errmsg, exc_info=ex)

    def unregister_observer(self, observer):
        """ unregister observer function """
        del self._observers[observer]
