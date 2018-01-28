# -*- coding: utf-8 -*-

"""Shared code simplifying plugin stuff."""

from importlib import import_module
from warnings import warn


def load_class(module_name, class_name):
    """Return class object specified by module name and class name.

    Return None if module failed to be imported.

    :param module_name: string module name
    :param class_name: string class name
    """
    try:
        plugmod = import_module(module_name)
    except Exception as exc:
        warn("Importing built-in plugin %s.%s raised an exception: %r" %
             (module_name, class_name, repr(exc)), ImportWarning)
        return None
    else:
        return getattr(plugmod, class_name)


def find_class(name, classes):
    """Return class in ``classes`` identified by configuration key ``name``."""
    name = name.lower()
    cls = next((c for c in classes if c.configuration_key == name), None)
    if cls is None:
        raise ValueError("No class named '%s' could be found" % name)
    return cls
