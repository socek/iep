# flake8: noqa
from sapp.plugins.sqlalchemy.alembic import AlembicScript

import iep
import venusian

from iep.application.drivers.dbmodel import SqlDataModel

# import or define all models here to ensure they are attached to the
# Model.metadata prior to any initialization routines

venusian.Scanner().scan(iep)

AlembicScript(iep.app, SqlDataModel, "dbsession").run()
