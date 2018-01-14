# -*- coding: utf-8 -*-

"""
Dynamic loading of built-in plugins.

All built-in plugins are listed here and will be dynamically imported
on importing this module. If importing a plugin fails, it will be ignored.
"""

from ..common.load import load_class as _load_plugin

_BUILTINS = ()

PLUGINS = {plug for plug in (_load_plugin(m, c) for m, c in _BUILTINS) if plug is not None}
