# -*- coding: utf-8 -*-

"""Management of updaters."""

from ..common.load import find_class


def updater_classes():
    """Return all built-in updater classes."""
    from .builtin import PLUGINS
    return PLUGINS


def get_updater_class(name="noip"):
    """Return updater class identified by configuration key ``name``."""
    return find_class(name, updater_classes())
