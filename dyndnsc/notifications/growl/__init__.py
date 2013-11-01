# -*- coding: utf-8 -*-

from ..base import Notification


def is_available():
    import sys
    if not sys.platform.startswith("darwin"):
        return False
    else:
        try:
            from .growl import Growl
        except ImportError:
            return False
        else:
            return True


def create_notify_handler():
    from .growl import Growl
    return Growl().create_notify_handler()

