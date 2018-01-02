# -*- coding: utf-8 -*-

"""
All built-in updater plugins are listed here and will be dynamically imported.

If importing a plugin fails, it will be silently ignored.
"""

from ..common.load import load_class as _load_plugin

_BUILTINS = (
    ("dyndnsc.updater.afraid", "UpdateProtocolAfraid"),
    ("dyndnsc.updater.dummy", "UpdateProtocolDummy"),
    ("dyndnsc.updater.duckdns", "UpdateProtocolDuckdns"),
    ("dyndnsc.updater.dyndns2", "UpdateProtocolDyndns2"),
    ("dyndnsc.updater.dnsimple", "UpdateProtocolDnsimple"),
)

PLUGINS = {plug for plug in (_load_plugin(m, c) for m, c in _BUILTINS) if plug is not None}
