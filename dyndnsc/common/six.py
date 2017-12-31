# -*- coding: utf-8 -*-

"""Module for providing python compatibility across interpreter versions."""

import sys
import inspect

# collect most py23 madness here
PY3 = sys.version_info[0] == 3
if PY3:
    getargspec = inspect.getfullargspec  # pylint: disable=invalid-name
    string_types = (str,)  # pylint: disable=invalid-name
    from io import StringIO  # noqa: @UnresolvedImport @UnusedImport pylint: disable=unused-import,import-error
else:
    getargspec = inspect.getargspec  # pylint: disable=invalid-name
    string_types = (basestring,)  # noqa: @UndefinedName pylint: disable=undefined-variable,invalid-name
    from cStringIO import StringIO  # noqa: @UnresolvedImport @UnusedImport pylint: disable=unused-import,import-error


if PY3:
    import ipaddress as _ipaddress

    def ipaddress(addr):
        """Return an ipaddress.ip_address object from the given string IP."""
        return _ipaddress.ip_address(addr)

    def ipnetwork(addr):
        """Return an ipaddress.ip_network object from the given string IP."""
        return _ipaddress.ip_network(addr)
else:
    import IPy as _IPy  # @UnresolvedImport pylint: disable=import-error

    def ipaddress(addr):
        """Return an IPy.IP object from the given string IP."""
        return _IPy.IP(addr)

    def ipnetwork(addr):
        """Return an IPy.IP object from the given string IP."""
        return _IPy.IP(addr)
