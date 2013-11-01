# -*- coding: utf-8 -*-

from ..base import Notification


def is_available():
    import sys
    if not sys.platform.startswith("darwin"):
        return False
    else:
        try:
            from .osxnotificationcenter import OSXNotification
        except ImportError:
            return False
        else:
            return True


def create_notify_handler():
    from .osxnotificationcenter import OSXNotification
    return OSXNotification().create_notify_handler()
