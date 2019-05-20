from .dbmodels import PanelTimeData
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel
from iep.conventions.drivers.query import ListActiveByConventionForModel


list_active = ListActiveForModel(PanelTimeData)
get_active_by_uid = GetActiveByUidForModel(PanelTimeData)
list_active_by_convention = ListActiveByConventionForModel(PanelTimeData)
