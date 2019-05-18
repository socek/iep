from .dbmodels import PanelData
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel
from iep.conventions.drivers.query import ListActiveByConventionForModel


list_active = ListActiveForModel(PanelData)
get_active_by_uid = GetActiveByUidForModel(PanelData)
list_active_by_convention = ListActiveByConventionForModel(PanelData)
