# -*- coding: utf-8 -*-


def updater_classes():
    from . import builtin
    return builtin.plugins


def find_class(name, classes):
    name = name.lower()
    for cls in classes:
        if name == cls.configuration_key():
            return cls
    raise KeyError("No class named '%s' could be found" % name)


def get_updater_class(name="noip"):
    return find_class(name, updater_classes())
