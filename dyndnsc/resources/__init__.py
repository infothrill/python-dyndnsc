# -*- coding: utf-8 -*-
"""
This package contains resources, non-python files, that we ship.
For ease of use, we provide this module to access the resources using
symbolic references, rather than by string conventions.
"""

from pkg_resources import resource_stream as _resstream  # @UnresolvedImport
from pkg_resources import resource_string as _resstring  # @UnresolvedImport
from pkg_resources import resource_exists as _resexists  # @UnresolvedImport
from pkg_resources import resource_filename as _resfname   # @UnresolvedImport


PRESETS_INI = "presets.ini"


def exists(resource_name):
    return _resexists(__name__, resource_name)


def getStream(resource_name):
    return _resstream(__name__, resource_name)


def getString(resource_name):
    return _resstring(__name__, resource_name)


def getFilename(resource_name):
    return _resfname(__name__, resource_name)
