# -*- coding: utf-8 -*-
"""
Problem to be solved: read and parse config file(s) and return something
useful for configuring one or more DynDnsClient(s)
"""

import logging
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


from .resources import getFilename, PROFILES_INI

log = logging.getLogger(__name__)

DEFAULT_USER_INI = ".dyndnsc.ini"


def getConfiguration(config_file=None):
    """
    Returns an initialized ConfigParser
    """
    parser = configparser.ConfigParser()
    if config_file is None:
        # fallback to default config file
        default_user_conf = os.path.join(os.getenv("HOME"), DEFAULT_USER_INI)
        config_file = default_user_conf
    assert os.path.isfile(config_file), "%s is not a file" % config_file

    configs = [getFilename(PROFILES_INI), config_file]
    log.debug("Attempting to read configuration from %r", configs)
    read_configs = parser.read(configs)
    log.debug("Successfully read configuration from %r", read_configs)
    log.debug(parser.sections())
    log.debug(parser.items('dyndnsc'))
    return parser
