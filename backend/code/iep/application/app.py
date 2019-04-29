from inspect import isfunction
from inspect import ismethod

from sapp.context import Context
from sapp.plugins.json import JsonPlugin
from sapp.plugins.logging import LoggingPlugin
from sapp.plugins.pyramid.configurator import ConfiguratorWithPyramid
from sapp.plugins.pyramid.plugins import RoutingPlugin
from sapp.plugins.settings import SettingsPlugin
from sapp.plugins.sqlalchemy.plugin import DatabasePlugin

from iep.application.plugins.routing import IAPRouting


class ContextGenerator(object):
    def __init__(self, configurator, args=None):
        self.configurator = configurator
        self.fun = self._extract_fun_from(args)
        self.args = args or []
        if self.fun:
            self.args = self.args[1:]

    def __enter__(self):
        ctx = self.configurator.__enter__()
        if len(self.args) == 0:
            return ctx
        elif len(self.args) == 1:
            return getattr(ctx, self.args[0])
        else:
            return [getattr(ctx, arg) for arg in self.args]

    def __exit__(self, *args, **kwargs):
        ctx = self.configurator.__exit__(*args, **kwargs)

    def _extract_fun_from(self, args):
        fun = len(args) == 1 and args[0] or None
        if fun and (isfunction(fun) or ismethod(fun)):
            return fun

    def __call__(self, *args, **kwargs):
        """
        This is called when Configurator is used as decorator.
        """
        fun = self._extract_fun_from(args)

        if fun:
            args = args[1:]

            def wrapper(*margs, **mkwargs):
                if len(self.args) <= 1:
                    # It was called as @app()
                    with self as ctx:
                        return fun(ctx, *margs, **mkwargs)
                else:
                    # It was called as @app(*args)
                    with self as ctx:
                        sargs = []
                        sargs.extend(ctx)
                        sargs.extend(margs)
                        return fun(*sargs, **mkwargs)

            return wrapper
        elif self.fun:
            # It was called as @app
            with self as ctx:
                return self.fun(ctx, *args, **kwargs)
        else:
            raise RuntimeError("You can not call an application!")


class IAPConfigurator(ConfiguratorWithPyramid):
    def append_plugins(self):
        self.add_plugin(SettingsPlugin("iep.application.settings"))
        self.add_plugin(LoggingPlugin())
        self.add_plugin(DatabasePlugin("dbsession"))
        self.add_plugin(RoutingPlugin(IAPRouting))
        self.add_plugin(JsonPlugin())

    def __call__(self, *args):
        return ContextGenerator(self, args)

    def __enter__(self):
        return self.create_context()

    def create_context(self):
        if not self.is_started:
            raise ConfiguratorNotStartedError(
                "Configurator is not started! Use Configurator.start(startpoint)"
            )

        self.context_count += 1
        if not self.context:
            self.context = Context(self)
            self.context.enter()
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        self.context_count -= 1
        if self.context_count == 0:
            self.context.exit(exc_type, exc_value, traceback)
