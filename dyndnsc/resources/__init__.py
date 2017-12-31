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
    """
    Test if the specified resource exists.

    :param resource_name: string
    """
    return _resexists(__name__, resource_name)


def get_stream(resource_name):
    """
    Return a stream of the specified resource.

    :param resource_name: string
    """
    return _resstream(__name__, resource_name)


def get_string(resource_name):
    """
    Return content string of the specified resource.

    :param resource_name: string
    """
    return _resstring(__name__, resource_name)


def get_filename(resource_name):
    """
    Return filename of the specified resource.

    :param resource_name: string
    """
    return _resfname(__name__, resource_name)
