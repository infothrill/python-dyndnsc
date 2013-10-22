# -*- coding: utf-8 -*-

"""
This provides Growl (http://growl.info/) notification support using the python
language bindings from Growl <= 1.1.2
"""

import logging


LOG = logging.getLogger(__name__)


def notify(sender, event, msg=None):
    '''
    Sends a notification to the growl subsystem
    '''
    LOG.debug("sender: %r, event: %r, msg: %r", sender, event, msg)
    _growlnotify(title=event, msg=msg)


def _growlnotify(title, msg):
    """Method to explicitly send a notification to the desktop of the user

    @param type: a notification type
    @param title: the title of the notification
    @param msg: the actual message
    """
    try:
        import Growl
    except ImportError:
        LOG.debug("No native growl support")
    else:
        __growlnotifier = Growl.GrowlNotifier(applicationName='dyndns', notifications=['User'], defaultNotifications=['User'])
        __growlnotifier.register()
        __growlnotifier.notify(noteType='User', title=title, description=msg)
