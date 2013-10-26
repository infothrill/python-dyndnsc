# -*- coding: utf-8 -*-

from .dyndns import UpdateProtocolDyndns
from .dummy import UpdateProtocolDummy
from .noip import UpdateProtocolNoip


def updaterClasses():
    from .base import UpdateProtocol
    return [cls for cls in UpdateProtocol.__subclasses__()]


def getUpdaterClass(protoname='dyndns'):
    """factory method to get the correct protocol Handler given its name"""
    for cls in updaterClasses():
        if cls.configuration_key() == protoname:
            return cls
    raise KeyError("No UpdateProtocol registered for '%s'", protoname)
