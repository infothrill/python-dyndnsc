# -*- coding: utf-8 -*-

"""Module with basic plugin code."""

import textwrap
import logging


log = logging.getLogger(__name__)

ENV_PREFIX = "DYNDNSC_WITH_"


class Plugin(object):

    """Base class for plugins.

    It is recommended but not *necessary* to
    subclass this class to create a plugin, but all plugins *must* implement
    `options(self, parser, env)` and `configure(self, options, conf)`, and
    must have the attributes `enabled` and `name`.

    A plugin should not be enabled by default.

    Subclassing Plugin (and calling the superclass methods in
    __init__, configure, and options, if you override them) will give
    your plugin some friendly default behavior:

    * A --with-$name option will be added to the command line interface
      to enable the plugin, and a corresponding environment variable
      will be used as the default value. The plugin class's docstring
      will be used as the help for this option.
    * The plugin will not be enabled unless this option is selected by
      the user.
    """

    can_configure = False
    enabled = False
    enableOpt = None
    name = None

    def __init__(self):
        if self.name is None:
            self.name = self.__class__.__name__.lower()
        if self.enableOpt is None:
            self.enableOpt = "enable_plugin_%s" % self.name.replace('-', '_')

    def options(self, parser, env):
        """Register commandline options with the given parser.

        Implement this method for normal options behavior with protection from
        OptionConflictErrors. If you override this method and want the default
        --with-$name option to be registered, be sure to call super().

        :param parser: argparse parser object
        :param env:
        """
        env_opt = ENV_PREFIX + self.name.upper()
        env_opt = env_opt.replace('-', '_')
        parser.add_argument("--with-%s" % self.name,
                            action="store_true",
                            dest=self.enableOpt,
                            default=env.get(env_opt),
                            help="Enable plugin %s: %s [%s]" %
                            (self.__class__.__name__, self.help(), env_opt))

    def configure(self, args):
        """Configure the plugin, based on selected options.

        The base plugin class sets the plugin to enabled if the enable option
        for the plugin (self.enableOpt) is true.
        """
        if not self.can_configure:
            return
        if hasattr(args, self.enableOpt):
            self.enabled = getattr(args, self.enableOpt)

    def help(self):
        """Return help for this plugin.

        This will be output as the help section of the --with-$name option
        that enables the plugin.
        """
        if self.__class__.__doc__:
            # doc sections are often indented; compress the spaces
            return textwrap.dedent(self.__class__.__doc__)
        return "(no help available)"


class IPluginInterface(object):

    """IPluginInterface describes the plugin API.

    Do not subclass or use this class directly.
    """

    def __new__(cls, *arg, **kw):
        """Private constructor."""
        raise TypeError("IPluginInterface class cannot be instantiated, it "
                        "is for documentation and API verification only")

    def options(self, parser, env):
        """Used to to register command line options with the argparse parser.

        DO NOT return a value from this method unless you want to stop
        all other plugins from setting their options.

        :param parser: options parser instance
        :type parser: :class:`argparse.ArgumentParser`
        :param env: environment, default is os.environ
        """
        pass

    def configure(self, options):
        """Called after any user input has been parsed, with the options.

        DO NOT return a value from this method unless you want to
        stop all other plugins from being configured.
        """
        pass

    def initialize(self):
        """Called before any core activities are run.

        Use this to perform any plugin specific setup.
        """
        pass

    def after_remote_ip_update(self, ip, status):
        pass
