from sapp import Decorator

from iep import app
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel

from .dbmodels import UserData

list_active = ListActiveForModel(UserData)
get_active_by_uid = GetActiveByUidForModel(UserData)


@Decorator(app, "dbsession")
def find_by_email(email, dbsession):
    """
    Get user model from database using email.
    """
    row = dbsession.query(UserData).filter(UserData.email == email).first()
    return row.to_model() if row else None
