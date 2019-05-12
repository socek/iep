from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel

from .dbmodels import ConventionData

list_active = ListActiveForModel(ConventionData)
get_active_by_uid = GetActiveByUidForModel(ConventionData)
