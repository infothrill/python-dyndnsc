# -*- coding: utf-8 -*-

from .growl import Growl


def create_notify_handler():
    return Growl().create_notify_handler()
