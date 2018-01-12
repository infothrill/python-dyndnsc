# -*- coding: utf-8 -*-

"""
All built-in detector plugins are listed here and will be dynamically imported.

If importing a plugin fails, it will be ignored.
"""

from ..common.load import load_class as _load_plugin

_BUILTINS = (
    ("dyndnsc.detector.command", "IPDetector_Command"),
    ("dyndnsc.detector.dns", "IPDetector_DNS"),
    ("dyndnsc.detector.dnswanip", "IPDetector_DnsWanIp"),
    ("dyndnsc.detector.iface", "IPDetector_Iface"),
    ("dyndnsc.detector.socket_ip", "IPDetector_Socket"),
    ("dyndnsc.detector.rand", "IPDetector_Random"),
    ("dyndnsc.detector.teredo", "IPDetector_Teredo"),
    ("dyndnsc.detector.webcheck", "IPDetectorWebCheck"),
    ("dyndnsc.detector.webcheck", "IPDetectorWebCheck6"),
    ("dyndnsc.detector.webcheck", "IPDetectorWebCheck46"),
)

PLUGINS = {plug for plug in (_load_plugin(m, c) for m, c in _BUILTINS) if plug is not None}
