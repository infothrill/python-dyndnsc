# -*- coding: utf-8 -*-

"""Management of detectors."""

from ..common.load import find_class


def detector_classes():
    """Return all built-in detector classes."""
    from .builtin import PLUGINS
    return PLUGINS


def get_detector_class(name="webcheck4"):
    """Return detector class identified by configuration key ``name``."""
    return find_class(name, detector_classes())
