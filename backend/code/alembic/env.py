# flake8: noqa
from sapp.plugins.sqlalchemy.alembic import AlembicScript

from iep import app
from iep.application.drivers.dbmodel import SqlDataModel

# import or define all models here to ensure they are attached to the
# Model.metadata prior to any initialization routines

AlembicScript(app, SqlDataModel, "dbsession").run()
