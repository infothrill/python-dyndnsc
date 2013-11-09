# -*- coding: utf-8 -*-

from .osxnotificationcenter import OSXNotification


def create_notify_handler():
    return OSXNotification().create_notify_handler()
