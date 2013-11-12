# -*- coding: utf-8 -*-


def detector_classes():
    from . import builtin
    return builtin.plugins


def get_detector_class(detector="webcheck"):
    detector = detector.lower()
    for cls in detector_classes():
        if cls.getName().lower() == detector:
            return cls
    raise KeyError("No IPDetector plugin named '%s' could be found" % detector)
