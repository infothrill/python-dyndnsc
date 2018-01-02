# -*- coding: utf-8 -*-

"""Observer/subject implementation."""

import logging

LOG = logging.getLogger(__name__)


class Subject(object):
    """Dispatches messages to registered callables."""

    def __init__(self):
        """Initialize."""
        self._observers = {}

    def register_observer(self, observer, events=None):
        """Register a listener function.

        :param observer: external listener function
        :param events: tuple or list of relevant events (default=None)
        """
        if events is not None and not isinstance(events, (tuple, list)):
            events = (events,)

        if observer in self._observers:
            LOG.warning("Observer '%r' already registered, overwriting for events"
                        " %r", observer, events)
        self._observers[observer] = events

    def notify_observers(self, event=None, msg=None):
        """Notify observers."""
        for observer, events in list(self._observers.items()):
            # LOG.debug("trying to notify the observer")
            if events is None or event is None or event in events:
                try:
                    observer(self, event, msg)
                except (Exception,) as ex:  # pylint: disable=broad-except
                    self.unregister_observer(observer)
                    errmsg = "Exception in message dispatch: Handler '{0}' unregistered for event '{1}'  ".format(
                        observer.__class__.__name__, event)
                    LOG.error(errmsg, exc_info=ex)

    def unregister_observer(self, observer):
        """Unregister observer callable."""
        del self._observers[observer]
