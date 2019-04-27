from unittest.mock import MagicMock
from unittest.mock import PropertyMock
from unittest.mock import patch
from uuid import uuid4

from pytest import fixture
from sapp.plugins.pyramid.testing import BaseWebTestFixture
from sapp.plugins.pyramid.testing import ViewFixtureMixin
from sapp.plugins.sqlalchemy.recreate import RecreateDatabases
from sapp.plugins.sqlalchemy.testing import BaseIntegrationFixture
from sqlalchemy.exc import InvalidRequestError

from iep.application.app import IAPConfigurator
from iep.auth.drivers import UserCommand
from iep.auth.drivers import UserQuery
from iep.auth.models import User


class DeleteOnExit(object):
    def __init__(self, dbsession, obj):
        self.obj = obj
        self.dbsession = dbsession

    def __enter__(self):
        self.dbsession.add(self.obj)
        self.dbsession.commit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.dbsession.delete(self.obj)
        try:
            self.dbsession.commit()
        except InvalidRequestError:
            self.dbsession.rollback()


class IAPFixturesMixin(object):
    CONFIGURATOR_CLASS = IAPConfigurator

    def after_configurator_start(self, config):
        paths = config.settings["paths"]
        recreate = RecreateDatabases(config)
        recreate.append_database("dbsession", paths["alembic:migrations"])
        recreate.make()

    user_data = {
        "name": "user1",
        "email": "user1@my.pl",
        "is_admin": False,
        "password": "mypassword",
    }

    second_user_data = {
        "name": "user2",
        "email": "user2@my.pl",
        "is_admin": False,
        "password": "mypassword",
    }

    wallet_data = {"name": "Wallet1", "type": "private"}
    second_wallet_data = {"name": "Wallet2", "type": "private"}

    contest_user_data = {"name": "contest1 from user1"}
    contest_second_user_data = {"name": "contest1 from user2"}

    game_user_data = {"name": "first game"}
    game_second_user_data = {"name": "second game"}

    group_data = {"name": "Group1"}
    second_group_data = {"name": "Group2"}

    @fixture(scope="class")
    def app(self, config):
        with config as app:
            yield app

    @fixture(scope="class")
    def dbsession(self, app):
        return app.dbsession

    @fixture(scope="class")
    def user_query(self, app):
        return UserQuery(app.dbsession)

    @fixture(scope="class")
    def user_command(self, app):
        return UserCommand(app.dbsession)

    @fixture(scope="class")
    def user(self, user_command, email=None):
        uid = uuid4()
        user_data = dict(self.user_data)
        user_data["email"] = email or user_data["email"]
        password_txt = user_data.pop("password")
        user = User(uid, **user_data)
        user.set_password(password_txt)
        user_command.create(user)
        yield user
        user_command.force_delete(uid)

    @fixture
    def dynamic_user(self, user_command):
        yield from self.user(user_command, "dynamic@gmail.com")

    @fixture(scope="class")
    def second_user(self, user_command):
        uid = uuid4()
        user_data = dict(self.second_user_data)
        password_txt = user_data.pop("password")
        user = User(uid, **user_data)
        user.set_password(password_txt)
        user_command.create(user)
        yield user
        user_command.force_delete(uid)


class IntegrationFixture(IAPFixturesMixin, BaseIntegrationFixture):
    pass


class WebTestFixture(IAPFixturesMixin, BaseWebTestFixture):
    login_url = "/auth/login"
    authenticated_user_data = {
        "name": "user3",
        "email": "user3@my.pl",
        "is_admin": False,
        "password": "mypassword",
    }

    @fixture
    def authenticated_user(self, dbsession, fake_app):
        user_data = dict(self.authenticated_user_data)
        password = user_data.pop("password")
        user = User(**user_data)
        user.set_password(password)

        with DeleteOnExit(dbsession, user):
            yield user

    @fixture
    def jwt(self, authenticated_user, fake_app):
        user_data = dict(self.authenticated_user_data)
        params = dict(email=user_data["email"], password=user_data["password"])
        result = fake_app.post_json(self.login_url, params=params, status=200)
        return result.json_body["jwt"]


class ViewFixture(ViewFixtureMixin):
    _view = None

    @fixture
    def view(self, mroot_factory, mrequest):
        return self._view(mroot_factory, mrequest)

    @fixture
    def mrequest(self):
        request = MagicMock()
        request._cache = {}
        return request

    @fixture
    def matchdict(self, mrequest):
        mrequest.matchdict = {}
        return mrequest.matchdict

    @fixture
    def mdbsession(self, view):
        with patch.object(self._view, "dbsession", new_callable=PropertyMock) as mock:
            yield mock.return_value

    @fixture
    def mget_user(self, view):
        with patch.object(view, "get_user", autospec=True) as mock:
            mock.return_value.uid = uuid4()
            yield mock
