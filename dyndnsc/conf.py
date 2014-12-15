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


def collect_config(cfg):
    collected_config = {}
    clientconfigs = [
        x.strip() for x in cfg.get("dyndnsc", "configs").split(",") if x.strip()]
    updaters = []
    for clientconfig in clientconfigs:
        logging.debug("client configuration: %r", clientconfig)
        clientcfg = dict(cfg.items(clientconfig))
        if cfg.has_option(clientconfig, "use_profile"):
            prf = dict(
                cfg.items("profile:" + cfg.get(clientconfig, "use_profile")))
            clientcfg.update(prf)
        else:
            # raw config with NO profile in use, so no updating of dict
            pass
        logging.debug(clientcfg)
        _det_str = "detector"
        detector_name = clientcfg.get(_det_str)
        detector_options = {}
        for k in clientcfg:
            if k.startswith(_det_str + "-"):
                detector_options[
                    k.replace(_det_str + "-", "")] = clientcfg[k]
        logging.debug(detector_options)
        collected_config[_det_str] = detector_name, detector_options
        _upd_str = "updater"
        updater_name = clientcfg.get(_upd_str)
        updater_options = {}
        for k in clientcfg:
            if k.startswith(_upd_str + "-"):
                updater_options[
                    k.replace(_upd_str + "-", "")] = clientcfg[k]
        logging.debug(updater_options)
        updaters.append((updater_name, updater_options))
        collected_config[_upd_str + "s"] = updaters
    return collected_config
