from iep import app

from .dbmodels import PanelData
from iep.application.drivers.query import GetByUidForModel
from iep.application.drivers.query import ListActiveForModel

list_active = ListActiveForModel(PanelData)
get_by_uid = GetByUidForModel(PanelData)
