from iep import app

from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel

from .dbmodels import RoomData

list_active = ListActiveForModel(RoomData)
get_active_by_uid = GetActiveByUidForModel(RoomData)
