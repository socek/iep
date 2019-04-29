# from iep.application.drivers import Query
from iep import app

from .dbmodels import PanelData


@app('dbsession')
def _list_active(db):
    return db.query(PanelData).filter(PanelData.is_active.is_(True))


def list_active():
    """
    Get list of all active panels.
    """
    for obj in _list_active():
        yield obj.to_dict()
