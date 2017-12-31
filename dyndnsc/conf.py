# -*- coding: utf-8 -*-

"""Problem to be solved: read and parse config file(s)."""

import logging
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


from .resources import get_filename, PRESETS_INI

LOG = logging.getLogger(__name__)

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
        if not os.path.isfile(config_file):
            raise ValueError("%s is not a file" % config_file)

    configs = [get_filename(PRESETS_INI)]
    if config_file:
        configs.append(config_file)
    LOG.debug("Attempting to read configuration from %r", configs)
    read_configs = parser.read(configs)
    LOG.debug("Successfully read configuration from %r", read_configs)
    LOG.debug("config file sections: %r", parser.sections())
    return parser


def _iraw_client_configs(cfg):
    """
    Generate (client_name, client_cfg_dict) tuples from the configuration.

    Conflates the presets and removes traces of the preset configuration
    so that the returned dict can be used directly on a dyndnsc factory.

    :param cfg: ConfigParser
    """
    client_names = cfg.get("dyndnsc", "configs").split(",")
    _preset_prefix = "preset:"
    _use_preset = "use_preset"
    for client_name in (x.strip() for x in client_names if x.strip()):
        client_cfg_dict = dict(cfg.items(client_name))
        if cfg.has_option(client_name, _use_preset):
            prf = dict(
                cfg.items(_preset_prefix + cfg.get(client_name, _use_preset)))
            prf.update(client_cfg_dict)
            client_cfg_dict = prf
        else:
            # raw config with NO preset in use, so no updating of dict
            pass
        logging.debug("raw config for '%s': %r", client_name, client_cfg_dict)
        if _use_preset in client_cfg_dict:
            del client_cfg_dict[_use_preset]
        yield client_name, client_cfg_dict


def collect_config(cfg):
    """
    Construct configuration dictionary from configparser.

    Resolves presets and returns a dictionary containing:

    .. code-block:: bash

        {
            "client_name": {
                "detector": ("detector_name", detector_opts),
                "updater": [
                    ("updater_name", updater_opts),
                    ...
                ]
            },
            ...
        }

    :param cfg: ConfigParser
    """
    collected_configs = {}
    _updater_str = "updater"
    _detector_str = "detector"
    _dash = "-"
    for client_name, client_cfg_dict in _iraw_client_configs(cfg):
        detector_name = None
        detector_options = {}
        updater_name = None
        updater_options = {}
        collected_config = {}
        for k in client_cfg_dict:
            if k.startswith(_detector_str + _dash):
                detector_options[
                    k.replace(_detector_str + _dash, "")] = client_cfg_dict[k]
            elif k == _updater_str:
                updater_name = client_cfg_dict.get(k)
            elif k == _detector_str:
                detector_name = client_cfg_dict.get(k)
            elif k.startswith(_updater_str + _dash):
                updater_options[
                    k.replace(_updater_str + _dash, "")] = client_cfg_dict[k]
            else:
                # options passed "as is" to the dyndnsc client
                collected_config[k] = client_cfg_dict[k]

        collected_config[_detector_str] = [(detector_name, detector_options)]
        collected_config[_updater_str] = [(updater_name, updater_options)]

        collected_configs[client_name] = collected_config
    return collected_configs
