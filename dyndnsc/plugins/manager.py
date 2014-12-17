# -*- coding: utf-8 -*-

import logging
from warnings import warn

from .base import IPluginInterface

log = logging.getLogger(__name__)


class PluginProxy(object):

    """Proxy for plugin calls.

    To verify presence of methods, this proxy is bound to an interface class
    providing no implementation.
    """

    interface = IPluginInterface

    def __init__(self, call, plugins):
        try:
            self.method = getattr(self.interface, call)
        except AttributeError:
            raise AttributeError("%s is not a valid %s method"
                                 % (call, self.interface.__name__))
        self.plugins = []
        for plugin in plugins:
            self.add_plugin(plugin, call)

    def __call__(self, *arg, **kw):
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
        for dummy, meth in self.plugins:
            result = meth(*arg, **kw)
            if result is not None:
                return result


class NullPluginManager(object):

    """Plugin manager that has no plugins.

    Used as a NOP when no plugins are used
    """

    interface = IPluginInterface

    def __iter__(self):
        return ()

    def __getattr__(self, call):
        return self._nop

    def _nop(self, *args, **kwds):
        pass

    def add_plugin(self, plug):
        raise NotImplementedError()

    def add_plugins(self, plugins):
        raise NotImplementedError()

    def configure(self, options):
        pass

    def load_plugins(self):
        pass


class PluginManager(object):

    """Base class PluginManager is not intended to be used directly.

    The basic functionality of a plugin manager is to proxy all unknown
    attributes through a ``PluginProxy`` to a list of plugins.

    The list of plugins *must not* be changed after the first call to a plugin.
    """

    proxyClass = PluginProxy

    def __init__(self, plugins=(), proxyClass=None):
        self._plugins = []
        self._proxies = {}
        if plugins:
            self.add_plugins(plugins)
        if proxyClass is not None:
            self.proxyClass = proxyClass

    def __getattr__(self, call):
        try:
            return self._proxies[call]
        except KeyError:
            proxy = self.proxyClass(call, self._plugins)
            self._proxies[call] = proxy
        return proxy

    def __iter__(self):
        return iter(self.plugins)

    def add_plugin(self, plugin):
        # allow plugins loaded via entry points to override builtin plugins
        new_name = getattr(plugin, 'name', object())
        self._plugins[:] = [p for p in self._plugins
                            if getattr(p, 'name', None) != new_name]
        self._plugins.append(plugin)

    def add_plugins(self, plugins=()):
        for plugin in plugins:
            self.add_plugin(plugin)

    def configure(self, args):
        """Configure the set of plugins with the given args.

        After configuration, disabled plugins are removed from the plugins list.
        """
        cfg = PluginProxy('configure', self._plugins)
        cfg(args)
        log.debug("Available plugins: %s", self._plugins)
        self.plugins = [plugin for plugin in self._plugins if plugin.enabled]
        log.debug("Enabled plugins: %s", self.plugins)

    def load_plugins(self):
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

    Load plugins from the setuptools entry_point `dyndnsc.plugins`s.
    """

    entry_points = ('dyndnsc.plugins-experimental',)

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
        from dyndnsc.plugins import builtin
        for plugin in builtin.plugins:
            self.add_plugin(plugin())
        super(BuiltinPluginManager, self).load_plugins()

try:
    import pkg_resources

    class DefaultPluginManager(EntryPointPluginManager, BuiltinPluginManager):
        pass

except ImportError:

    class DefaultPluginManager(BuiltinPluginManager):
        pass
