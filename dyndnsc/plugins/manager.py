# -*- coding: utf-8 -*-

"""Module for plugin manager."""

import logging
from warnings import warn

from .base import IPluginInterface

ENV_PREFIX = "DYNDNSC_WITH_"
LOG = logging.getLogger(__name__)


class PluginProxy(object):
    """Proxy for plugin calls.

    To verify presence of methods, this proxy is bound to an interface class
    providing no implementation.
    """

    interface = IPluginInterface

    def __init__(self, call, plugins):
        """Initialize the given plugins."""
        try:
            self.method = getattr(self.interface, call)
        except AttributeError:
            raise AttributeError("%s is not a valid %s method"
                                 % (call, self.interface.__name__))
        self.plugins = []
        for plugin in plugins:
            self.add_plugin(plugin, call)

    def __call__(self, *arg, **kw):
        """Implement callable interface by calling every plugin sequentally."""
        return self.listcall(*arg, **kw)

    def add_plugin(self, plugin, call):
        """Add plugin to list of plugins.

        Will be added if it has the attribute I'm bound to.
        """
        meth = getattr(plugin, call, None)
        if meth is not None:
            self.plugins.append((plugin, meth))

    def listcall(self, *arg, **kw):
        """Call each plugin sequentially.

        Return the first result that is not None.
        """
        final_result = None
        for _, meth in self.plugins:
            result = meth(*arg, **kw)
            if final_result is None and result is not None:
                final_result = result
        return final_result


class NullPluginManager(object):
    """Plugin manager that has no plugins.

    Used as a NOP when no plugins are used
    """

    interface = IPluginInterface

    def __iter__(self):
        """Return an empty iterator."""
        return iter(())

    def __getattr__(self, call):
        """Return a dummy function that does nothing regardless of specified args."""
        return self._nop

    def _nop(self, *args, **kwds):
        pass

    def add_plugin(self, plug):
        """Fake add plugin to list of plugins."""
        raise NotImplementedError()

    def add_plugins(self, plugins):
        """Fake add plugins to list of plugins."""
        raise NotImplementedError()

    def configure(self, options):
        """Fake configure plugins."""
        pass

    def load_plugins(self):
        """Fake load plugins."""
        pass


class PluginManager(object):
    """Base class PluginManager is not intended to be used directly.

    The basic functionality of a plugin manager is to proxy all unknown
    attributes through a ``PluginProxy`` to a list of plugins.

    The list of plugins *must not* be changed after the first call to a plugin.
    """

    proxyClass = PluginProxy

    def __init__(self, plugins=(), proxyClass=None):
        """Initialize."""
        self._plugins = []
        self._proxies = {}
        if plugins:
            self.add_plugins(plugins)
        if proxyClass is not None:
            self.proxyClass = proxyClass

    def __getattr__(self, call):
        """Return proxy method for all plugins for call."""
        try:
            return self._proxies[call]
        except KeyError:
            proxy = self.proxyClass(call, self._plugins)
            self._proxies[call] = proxy
        return proxy

    def __iter__(self):
        """Return an iterator over all registered plugins."""
        return iter(self.plugins)

    def add_plugin(self, plugin):
        """Add the given plugin."""
        # allow plugins loaded via entry points to override builtin plugins
        new_name = self.plugin_name(plugin)
        self._plugins[:] = [p for p in self._plugins
                            if self.plugin_name(p) != new_name]
        self._plugins.append(plugin)

    @staticmethod
    def plugin_name(plugin):
        """Discover the plugin name and return it."""
        return plugin.__class__.__name__.lower()

    def add_plugins(self, plugins=()):
        """Add the given plugins."""
        for plugin in plugins:
            self.add_plugin(plugin)

    def configure(self, args):
        """Configure the set of plugins with the given args.

        After configuration, disabled plugins are removed from the plugins list.
        """
        for plug in self._plugins:
            plug_name = self.plugin_name(plug)
            plug.enabled = getattr(args, "plugin_%s" % plug_name, False)
            if plug.enabled and getattr(plug, "configure", None):
                if callable(getattr(plug, "configure", None)):
                    plug.configure(args)
        LOG.debug("Available plugins: %s", self._plugins)
        self.plugins = [plugin for plugin in self._plugins if getattr(plugin, "enabled", False)]
        LOG.debug("Enabled plugins: %s", self.plugins)

    def options(self, parser, env):
        """Register commandline options with the given parser.

        Implement this method for normal options behavior with protection from
        OptionConflictErrors. If you override this method and want the default
        --with-$name option to be registered, be sure to call super().

        :param parser: argparse parser object
        :param env:
        """
        def get_help(plug):
            """Extract the help docstring from the given plugin."""
            import textwrap
            if plug.__class__.__doc__:
                # doc sections are often indented; compress the spaces
                return textwrap.dedent(plug.__class__.__doc__)
            return "(no help available)"
        for plug in self._plugins:
            env_opt = ENV_PREFIX + self.plugin_name(plug).upper()
            env_opt = env_opt.replace("-", "_")
            parser.add_argument("--with-%s" % self.plugin_name(plug),
                                action="store_true",
                                dest="plugin_%s" % self.plugin_name(plug),
                                default=env.get(env_opt),
                                help="Enable plugin %s: %s [%s]" %
                                (plug.__class__.__name__, get_help(plug), env_opt))

    def load_plugins(self):
        """Abstract method."""
        pass

    def _get_plugins(self):
        return self._plugins

    def _set_plugins(self, plugins):
        self._plugins = []
        self.add_plugins(plugins)

    plugins = property(
        _get_plugins, _set_plugins, None, """Access the list of plugins""")


class EntryPointPluginManager(PluginManager):
    """Plugin manager.

    Load plugins from the setuptools entry_point ``dyndnsc.plugins``.
    """

    entry_points = ("dyndnsc.notifier_beta",)

    def load_plugins(self):
        """Load plugins from entry point(s)."""
        from pkg_resources import iter_entry_points
        seen = set()
        for entry_point in self.entry_points:
            for ep in iter_entry_points(entry_point):
                if ep.name in seen:
                    continue
                seen.add(ep.name)
                try:
                    plugincls = ep.load()
                except Exception as exc:
                    # never let a plugin load kill us
                    warn("Unable to load plugin %s: %s" % (ep, exc),
                         RuntimeWarning)
                    continue
                plugin = plugincls()
                self.add_plugin(plugin)
        super(EntryPointPluginManager, self).load_plugins()


class BuiltinPluginManager(PluginManager):
    """Plugin manager.

    Load plugins from the list in `dyndnsc.plugins.builtin`.
    """

    def load_plugins(self):
        """Load plugins from `dyndnsc.plugins.builtin`."""
        from dyndnsc.plugins.builtin import PLUGINS
        for plugin in PLUGINS:
            self.add_plugin(plugin())
        super(BuiltinPluginManager, self).load_plugins()


try:
    import pkg_resources  # noqa: @UnusedImport pylint: disable=unused-import

    class DefaultPluginManager(EntryPointPluginManager, BuiltinPluginManager):
        """The plugin manager serving both built-in and external plugins."""

        pass

except ImportError:

    class DefaultPluginManager(BuiltinPluginManager):
        """The plugin manager serving only built-in plugins."""

        pass
