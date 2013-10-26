# -*- coding: utf-8 -*-

from .impl import IPDetector, IPDetector_DNS, IPDetector_Command, IPDetector_Random, \
                  IPDetector_Iface, IPDetector_WebCheck, IPDetector_Teredo


def detectorClasses():
    return [cls for cls in IPDetector.__subclasses__()]


def getDetectorClass(detector="webcheck"):
    detector = detector.lower()
    for cls in detectorClasses():
        if cls.getName().lower() == detector:
            return cls
    raise KeyError("No IPDetector class for '%s' registered" % detector)
