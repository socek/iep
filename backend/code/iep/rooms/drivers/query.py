from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel
from iep.conventions.drivers.query import ListActiveByConventionForModel

from .dbmodels import RoomData


list_active = ListActiveForModel(RoomData)
get_active_by_uid = GetActiveByUidForModel(RoomData)
list_active_by_convention = ListActiveByConventionForModel(RoomData)
