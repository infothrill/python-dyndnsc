# -*- coding: utf-8 -*-

from .dyndns import UpdateProtocolDyndns
from .dummy import UpdateProtocolDummy
from .noip import UpdateProtocolNoip
from .nsupdate_info import UpdateProtocolNsUpdate

import logging

log = logging.getLogger(__name__)


def updaterClasses():
    from .base import UpdateProtocol
    return [cls for cls in UpdateProtocol.__subclasses__()]  # + updaterClasses_external()


def updaterClasses_external():
    '''
    Tentative support for external plugins
    '''
    from pkg_resources import iter_entry_points
    for ep in iter_entry_points(group='dyndnsc.updater_builtin', name=None):
        log.warn("%s, %s", ep, type(ep))
        log.warn("%s %s %s %s %s", ep.name, ep.dist, ep.module_name, ep.attrs, ep.extras)
    return [ep.load() for ep in iter_entry_points(group='dyndnsc.updater', name=None)]


def getUpdaterClass(protoname='dyndns'):
    """factory method to get the correct protocol Handler given its name"""
    for cls in updaterClasses():
        if cls.configuration_key() == protoname:
            return cls
    raise KeyError("No UpdateProtocol registered for '%s'", protoname)
