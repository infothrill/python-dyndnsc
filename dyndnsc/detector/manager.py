# -*- coding: utf-8 -*-


def detector_classes():
    from . import builtin
    return builtin.plugins


def find_class(name, classes):
    name = name.lower()
    for cls in classes:
        if name == cls.configuration_key():
            return cls
    raise KeyError("No class named '%s' could be found" % name)


def get_detector_class(name="webcheck"):
    return find_class(name, detector_classes())
