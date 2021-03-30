# -*- coding: utf-8 -*-

"""Module for providing python compatibility across interpreter versions."""

import inspect
import ipaddress as _ipaddress

getargspec = inspect.getfullargspec  # pylint: disable=invalid-name
string_types = (str,)  # pylint: disable=invalid-name
from io import StringIO  # noqa: @UnresolvedImport @UnusedImport pylint: disable=unused-import,import-error


def ipaddress(addr):
    """Return an ipaddress.ip_address object from the given string IP."""
    return _ipaddress.ip_address(addr)


def ipnetwork(addr):
    """Return an ipaddress.ip_network object from the given string IP."""
    return _ipaddress.ip_network(addr)
