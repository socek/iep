from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import sentinel

from pytest import fixture
from pytest import raises
from sapp.configurator import Configurator
from sapp.configurator import ConfiguratorNotStartedError
from sapp.plugin import Plugin

from iep.application.app import BaseIAPConfigurator


class ExamplePlugin(Plugin):
    def __init__(self, name):
        self.name = name

    def start(self, configurator):
        pass

    def enter(self, context):
        setattr(context, self.name, getattr(sentinel, self.name))


class ExampleConfigurator(BaseIAPConfigurator):
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


class ExampleConfigurator2(BaseIAPConfigurator):
    def append_plugins(self):
        super().append_plugins()
        self.plugin1 = MagicMock()
        self.plugin2 = MagicMock()

        self.add_plugin(self.plugin1)
        self.add_plugin(self.plugin2)


class TestConfigurator(object):
    @fixture
    def configurator(self):
        return ExampleConfigurator2()

    def test_configurator_on_not_started(self, configurator):
        """
        Configurator should raise an error when it will be used without starting
        it in the first place.
        """
        with raises(ConfiguratorNotStartedError):
            with configurator:
                pass

    def test_start(self, configurator):
        """
        .start should append plugins and init them. Also proper flags should be
        set.
        """
        configurator.start("wsgi", wsgi=1)

        assert configurator.extra == {"wsgi": 1}
        assert configurator.startpoint == "wsgi"
        assert configurator.is_started

        configurator.plugin1.start.assert_called_once_with(configurator)
        configurator.plugin2.start.assert_called_once_with(configurator)

        assert configurator.plugins == [configurator.plugin1, configurator.plugin2]

    def test_context_manager_many_times(self, configurator):
        """
        Using configurator as context manager should enter and exit plugins only
        once.
        """
        configurator.start()

        with configurator as app:
            with configurator as app:
                configurator.plugin1.enter.assert_called_once_with(app)
                configurator.plugin2.enter.assert_called_once_with(app)

        configurator.plugin1.start.assert_called_once_with(configurator)
        configurator.plugin2.start.assert_called_once_with(configurator)

        configurator.plugin1.exit.assert_called_once_with(app, None, None, None)
        configurator.plugin2.exit.assert_called_once_with(app, None, None, None)

    def test_context_manager_when_raised(self, configurator):
        """
        When using configurator as context manager and an exception is raised,
        all plugins should get that exception.
        """
        configurator.start()
        error = RuntimeError()

        with raises(RuntimeError):
            with configurator as app:
                raise error

        configurator.plugin1.start.assert_called_once_with(configurator)
        configurator.plugin2.start.assert_called_once_with(configurator)

        call = configurator.plugin1.exit.call_args_list[0][0]
        assert call[0] == app
        assert call[1] == RuntimeError
        assert call[2] == error
        assert call[3] is not None

        call = configurator.plugin2.exit.call_args_list[0][0]
        assert call[0] == app
        assert call[1] == RuntimeError
        assert call[2] == error
        assert call[3] is not None

    def test_mocking(self, configurator):
        """
        Mocking the application objects should be simple an easy.
        """
        with patch.object(configurator, "create_context") as mock:
            with configurator as app:
                assert app == mock.return_value


class ExamplePlugin2(object):
    def start(self, configurator):
        pass

    def enter(self, context):
        context.first = sentinel.first

    def exit(self, *args, **kwargs):
        pass


class ExampleSecondPlugin(ExamplePlugin2):
    def enter(self, context):
        print("b")
        context.second = sentinel.second


class ExampleThirdPlugin(ExamplePlugin2):
    def enter(self, context):
        print("c")
        context.third = sentinel.third


class ExampleSecondConfigurator(BaseIAPConfigurator):
    def append_plugins(self):
        super().append_plugins()
        self.add_plugin(ExamplePlugin2())
        self.add_plugin(ExampleSecondPlugin())
        self.add_plugin(ExampleThirdPlugin())


class TestFragmentContext(object):
    @fixture
    def configurator(self):
        return ExampleSecondConfigurator()

    def test_no_parametr(self, configurator):
        """
        Configuratior should be able to give normal context if no parameteres
        gived.
        """
        configurator.start()
        with configurator() as ctx:
            assert ctx.second == sentinel.second

    def test_one_parametr(self, configurator):
        """
        Configuratior should be able to give context only of the choosed
        parameters as a one.
        """
        configurator.start()
        with configurator("second") as second:
            assert second == sentinel.second

    def test_two_parameters(self, configurator):
        """
        Configuratior should be able to give context only of the choosed
        parameters as a list.
        """
        configurator.start()
        with configurator("first", "third") as (first, third):
            assert first == sentinel.first
            assert third == sentinel.third
