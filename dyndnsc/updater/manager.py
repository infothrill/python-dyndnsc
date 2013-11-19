# -*- coding: utf-8 -*-


def updater_classes():
    from . import builtin
    return builtin.plugins


def get_updater_class(updater="noip"):
    updater = updater.lower()
    for cls in updater_classes():
        if updater == cls.configuration_key():
            return cls
    raise KeyError("No Updater plugin named '%s' could be found" % updater)
