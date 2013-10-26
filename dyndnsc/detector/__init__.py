# -*- coding: utf-8 -*-

from .base import IPDetector
from .dns import IPDetector_DNS
from .command import IPDetector_Command
from .rand import IPDetector_Random
from .iface import IPDetector_Iface
from .webcheck import IPDetector_WebCheck
from .teredo import IPDetector_Teredo


def detectorClasses():
    return [cls for cls in IPDetector.__subclasses__()]


def getDetectorClass(detector="webcheck"):
    detector = detector.lower()
    for cls in detectorClasses():
        if cls.getName().lower() == detector:
            return cls
    raise KeyError("No IPDetector class for '%s' registered" % detector)
