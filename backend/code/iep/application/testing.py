from unittest.mock import MagicMock
from unittest.mock import PropertyMock
from unittest.mock import patch
from uuid import uuid4

from alembic import command
from alembic.config import Config
from pytest import fixture
from sapp.plugins.pyramid.testing import BaseWebTestFixture
from sapp.plugins.pyramid.testing import ViewFixtureMixin
from sapp.plugins.sqlalchemy.recreate import RecreateDatabases
from sapp.plugins.sqlalchemy.testing import BaseIntegrationFixture
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker

from iep import app
from iep.application.app import ContextManager
from iep.application.app import IAPConfigurator
from iep.auth.drivers import command as user_command
from iep.auth.drivers import query as user_query
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


class ImprovedRecreateDatabases(RecreateDatabases):
    def _clear_database(self, database):
        """
        In order to drop database, we need to connect to another one (using
        default_url). With that connection we need to drop and create new
        database.
        """
        dbname = database.get_dbname()
        engine = database.get_engine(default_url=True)
        session = sessionmaker(bind=engine)()
        session.connection().connection.set_isolation_level(0)
        # session.execute(
        #     "UPDATE pg_database SET datallowconn = 'false' WHERE datname = '{}}';".format(
        #         dbname
        #     )
        # )
        session.execute(
            """SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{}' -- ← change this to your DB
                  AND pid <> pg_backend_pid();""".format(
                dbname
            )
        )
        session.execute("DROP DATABASE IF EXISTS {}".format(dbname))
        session.execute("CREATE DATABASE {}".format(dbname))
        session.close()


class IAPFixturesMixin(object):
    CONFIGURATOR_CLASS = IAPConfigurator

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

    def _create_user(self, email=None):
        user_data = dict(self.user_data)
        user_data["email"] = email or user_data["email"]
        password_txt = user_data.pop("password")
        user = User(None, **user_data)
        user.set_password(password_txt)
        return user.to_dict()

    @fixture(scope="class")
    def user(self):
        uid = user_command.save_new(**self._create_user())
        yield user_query.get_by_uid(uid)
        user_command.force_delete(uid)

    @fixture
    def dynamic_user(self):
        uid = user_command.save_new(**self._create_user("dynamic@gmail.com"))
        yield user_query.get_by_uid(uid)
        user_command.force_delete(uid)

    @fixture(scope="class")
    def second_user(self):
        user_data = dict(self.second_user_data)
        password_txt = user_data.pop("password")
        user = User(None, **user_data)
        user.set_password(password_txt)
        uid = user_command.create(user.to_dict())
        yield user_query.get_by_uid(uid)
        user_command.force_delete(uid)


class IntegrationFixture(IAPFixturesMixin):
    SESSION_CACHE = {}
    CONFIGURATOR_KEY = 'app'

    def after_configurator_start(self, app):
        paths = app.settings["paths"]
        recreate = ImprovedRecreateDatabases(app)
        recreate.append_database("dbsession", paths["alembic:migrations"])
        recreate.make()

    @fixture(scope="module", autouse=True)
    def config(self):
        """
        This fixture will create full configurator object. It can be use for
        accessing app during the tests.
        """
        if self.CONFIGURATOR_KEY not in self.SESSION_CACHE:
            app.start('tests')
            self.SESSION_CACHE[self.CONFIGURATOR_KEY] = app
            self.after_configurator_start(app)
        return self.SESSION_CACHE[self.CONFIGURATOR_KEY]



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
