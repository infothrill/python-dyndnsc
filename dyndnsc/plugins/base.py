# -*- coding: utf-8 -*-

"""Module with basic plugin code."""

import logging


LOG = logging.getLogger(__name__)


class IPluginInterface(object):
    """IPluginInterface describes the plugin API.

    Do not subclass or use this class directly.
    """

    def __new__(cls, *arg, **kw):
        """Private constructor."""
        raise TypeError("IPluginInterface class cannot be instantiated, it "
                        "is for documentation and API verification only")

    def options(self, parser, env):
        """Register command line options with the argparse parser.

        DO NOT return a value from this method unless you want to stop
        all other plugins from setting their options.

        :param parser: options parser instance
        :type parser: `argparse.ArgumentParser`
        :param env: environment, default is os.environ
        """
        pass

    def configure(self, options):
        """Call after any user input has been parsed, with the options.

        DO NOT return a value from this method unless you want to
        stop all other plugins from being configured.
        """
        pass

    def initialize(self):
        """Call before any core activities are run.

        Use this to perform any plugin specific setup.
        """
        pass

    def after_remote_ip_update(self, ip, status):
        """Call after a remote IP update was performed."""
