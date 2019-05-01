from collections import Iterable
from inspect import isfunction
from inspect import ismethod

from sapp.configurator import ConfiguratorNotStartedError
from sapp.context import Context
from sapp.plugins.json import JsonPlugin
from sapp.plugins.logging import LoggingPlugin
from sapp.plugins.pyramid.configurator import ConfiguratorWithPyramid
from sapp.plugins.pyramid.plugins import RoutingPlugin
from sapp.plugins.settings import SettingsPlugin
from sapp.plugins.sqlalchemy.plugin import DatabasePlugin

from iep.application.plugins.routing import IAPRouting


class BaseIAPConfigurator(ConfiguratorWithPyramid):
    def __init__(self):
        self.is_started = False
        self.startpoint = None
        self.plugins = []

        self.context_count = 0
        self.context = None

    def _start_plugins(self):
        for plugin in self.plugins:
            plugin.start(self)

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def _enter_context(self):
        self.context_count += 1
        if not self.context:
            self.context = Context(self)
            self.context.enter()
        return self.context

    def _exit_context(self, exc_type, exc_value, traceback):
        self.context_count -= 1
        if self.context_count == 0:
            self.context.exit(exc_type, exc_value, traceback)


class ContextManager(object):
    def __init__(self, application, values=[]):
        self.application = application
        self.values = values
        self.context = None

    def __enter__(self):
        ctx = self.application._enter_context()
        if not self.values:
            return ctx
        elif isinstance(self.values, str):
            return getattr(ctx, self.values)
        elif isinstance(self.values, Iterable):
            return [getattr(ctx, key) for key in self.values]
        else:
            raise RuntimeError("Wrong argument type!")

    def __exit__(self, exc_type, exc_value, traceback):
        self.application._exit_context(exc_type, exc_value, traceback)


class Decorator(object):
    def __init__(self, application, values=[]):
        self.application = application
        self.values = values
        self.context = None

    def __call__(self, fun):
        def wrapper(*args, **kwargs):
            ctx = self.application._enter_context()
            kwargs = dict(kwargs)
            try:
                if self.values == []:
                    if "ctx" not in kwargs:
                        kwargs["ctx"] = ctx
                elif isinstance(self.values, str):
                    kwargs[self.values] = getattr(ctx, self.values)
                elif isinstance(self.values, Iterable):
                    for key in self.values:
                        if key not in kwargs:
                            kwargs[key] = getattr(ctx, key)
                else:
                    raise RuntimeError("Wrong argument type!")
                return fun(*args, **kwargs)
            finally:
                # TODO: we probably need to pass here something
                self.application._exit_context(None, None, None)

        return wrapper
    # ---------------------------


class IAPConfigurator(BaseIAPConfigurator):
    def append_plugins(self):
        self.add_plugin(SettingsPlugin("iep.application.settings"))
        self.add_plugin(LoggingPlugin())
        self.add_plugin(DatabasePlugin("dbsession"))
        self.add_plugin(RoutingPlugin(IAPRouting))
        self.add_plugin(JsonPlugin())
