# -*- coding: utf-8 -*-

"""
All built-in updater plugins are listed here and will be dynamically imported
on importing this module. If importing a plugin fails, it will be ignored.
"""

from importlib import import_module
from warnings import warn

_builtins = (
    ('dyndnsc.updater.afraid', 'UpdateProtocolAfraid'),
    ('dyndnsc.updater.dummy', 'UpdateProtocolDummy'),
    ('dyndnsc.updater.dyndns2', 'UpdateProtocolDyndns2'),
    ('dyndnsc.updater.dnsimple', 'UpdateProtocolDnsimple'),
)


def _load_plugin(module, cls):
    """
    Try to load one plugin, return None if it failed to load
    :param module: module name
    :param cls: class name
    """
    try:
        plugmod = import_module(module)
    except Exception as exc:
        warn("Importing built-in plugin %s.%s raised an exception: %r" %
             (module, cls, repr(exc)), ImportWarning)
        return None
    else:
        return getattr(plugmod, cls)


def _iload_plugins(builtins):
    """
    return a generator for all 'importable' built-in plugins
    :param builtins: set of tuples(modulename, classname)
    """
    for m, c in builtins:
        plugcls = _load_plugin(m, c)
        if plugcls is not None:
            yield plugcls

plugins = set((_plugcls for _plugcls in _iload_plugins(_builtins)))
