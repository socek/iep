from unittest.mock import sentinel

from pytest import fixture
from pytest import raises
from sapp.plugin import Plugin

from iep.application.app import IAPConfigurator


class ExamplePlugin(Plugin):
    def __init__(self, name):
        self.name = name

    def start(self, configurator):
        pass

    def enter(self, context):
        setattr(context, self.name, getattr(sentinel, self.name))


class ExampleConfigurator(IAPConfigurator):
    def append_plugins(self):
        self.add_plugin(ExamplePlugin("first"))
        self.add_plugin(ExamplePlugin("second"))
        self.add_plugin(ExamplePlugin("third"))


class TestApplication(object):
    """
    Check if all possible Configurator uses are up and running.
    """

    @fixture
    def app(self):
        app = ExampleConfigurator()
        app.start("start")
        return app

    def test_as_context_manager(self, app):
        with app as context:
            assert context.first == sentinel.first
            assert context.second == sentinel.second

    def test_as_context_manager_call(self, app):
        with app() as context:
            assert context.first == sentinel.first
            assert context.second == sentinel.second

    def test_as_context_manager_call_with_argument(self, app):
        with app("first") as first:
            assert first == sentinel.first

    def test_as_context_manager_call_with_arguments(self, app):
        with app("first", "second") as (first, second):
            assert first == sentinel.first
            assert second == sentinel.second

    def test_as_decorator(self, app):
        @app
        def fun(context, arg):
            assert arg == sentinel.arg
            assert context.first == sentinel.first
            assert context.second == sentinel.second

        fun(sentinel.arg)

    def test_as_decorator_call(self, app):
        @app()
        def fun(context, arg):
            assert arg == sentinel.arg
            assert context.first == sentinel.first
            assert context.second == sentinel.second

        fun(sentinel.arg)

    def test_as_decorator_call_with_argument(self, app):
        @app("first")
        def fun(first, arg):
            assert arg == sentinel.arg
            assert first == sentinel.first

        fun(sentinel.arg)

    def test_as_decorator_call_with_arguments(self, app):
        @app("first", "second")
        def fun(first, second, arg):
            assert arg == sentinel.arg
            assert first == sentinel.first
            assert second == sentinel.second

        fun(sentinel.arg)

    def test_as_function_generator(self, app):
        with raises(RuntimeError):
            app()()
