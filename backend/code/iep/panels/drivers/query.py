# from iep.application.drivers import Query
from iep import app

from .dbmodels import PanelData
from iep.application.app import Decorator


@Decorator(app, "dbsession")
def _list_active(dbsession):
    return dbsession.query(PanelData).filter(PanelData.is_active.is_(True))


def list_active():
    """
    Get list of all active panels.
    """
    for obj in _list_active():
        yield obj.to_dict()
