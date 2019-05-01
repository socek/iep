from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel

from .dbmodels import PanelData

save_new = SaveNewForModel(PanelData)
update_by_uid = UpdateByIdForModel(PanelData)
delete_by_uid = DeleteByIdForModel(PanelData)
force_delete = ForceDeleteForModel(PanelData)
