from iep import Decorator
from iep import app
from iep.application.drivers.query import GetByUidForModel
from iep.application.drivers.query import ListActiveForModel

from .dbmodels import UserData

list_active = ListActiveForModel(UserData)
get_by_uid = GetByUidForModel(UserData)


@Decorator(app, "dbsession")
def find_by_email(email, dbsession):
    row = dbsession.query(UserData).filter(UserData.email == email).first()
    return row.to_model() if row else None
