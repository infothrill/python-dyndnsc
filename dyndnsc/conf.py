# -*- coding: utf-8 -*-

"""Problem to be solved: read and parse config file(s)."""

import logging
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


from .resources import getFilename, PRESETS_INI

log = logging.getLogger(__name__)

DEFAULT_USER_INI = ".dyndnsc.ini"


def get_configuration(config_file=None):
    """Return an initialized ConfigParser.

    If no config filename is presented, `DEFAULT_USER_INI` is used if present.
    Also reads the built-in presets.

    :param config_file: string path
    """
    parser = configparser.ConfigParser()
    if config_file is None:
        # fallback to default user config file
        config_file = os.path.join(os.getenv("HOME"), DEFAULT_USER_INI)
        if not os.path.isfile(config_file):
            config_file = None
    else:
        assert os.path.isfile(config_file), "%s is not a file" % config_file

    configs = [getFilename(PRESETS_INI)]
    if config_file:
        configs.append(config_file)
    log.debug("Attempting to read configuration from %r", configs)
    read_configs = parser.read(configs)
    log.debug("Successfully read configuration from %r", read_configs)
    log.debug("config file sections: %r", parser.sections())
    return parser


def collect_config(cfg):
    collected_configs = {}
    clientconfigs = [
        x.strip() for x in cfg.get("dyndnsc", "configs").split(",") if x.strip()]
    updaters = []
    for clientconfig in clientconfigs:
        collected_configs[clientconfig] = {}
        logging.debug("client configuration: %r", clientconfig)
        clientcfg = dict(cfg.items(clientconfig))
        if cfg.has_option(clientconfig, "use_preset"):
            prf = dict(
                cfg.items("preset:" + cfg.get(clientconfig, "use_preset")))
            clientcfg.update(prf)
        else:
            # raw config with NO preset in use, so no updating of dict
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
        collected_configs[clientconfig][_det_str] = detector_name, detector_options
        _upd_str = "updater"
        updater_name = clientcfg.get(_upd_str)
        updater_options = {}
        for k in clientcfg:
            if k.startswith(_upd_str + "-"):
                updater_options[
                    k.replace(_upd_str + "-", "")] = clientcfg[k]
        logging.debug(updater_options)
        updaters.append((updater_name, updater_options))
        collected_configs[clientconfig][_upd_str + "s"] = updaters
    return collected_configs
