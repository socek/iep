from iep import app

from .dbmodels import PanelData
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel

list_active = ListActiveForModel(PanelData)
get_active_by_uid = GetActiveByUidForModel(PanelData)
