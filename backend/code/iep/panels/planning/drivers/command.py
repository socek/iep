from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel

from .dbmodels import PanelTimeData

save_new = SaveNewForModel(PanelTimeData)
update_by_uid = UpdateByIdForModel(PanelTimeData)
delete_by_uid = DeleteByIdForModel(PanelTimeData)
force_delete = ForceDeleteForModel(PanelTimeData)
