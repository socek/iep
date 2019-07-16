from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel

from .dbmodels import Guest2PanelData

save_new = SaveNewForModel(Guest2PanelData)
update_by_uid = UpdateByIdForModel(Guest2PanelData)
delete_by_uid = DeleteByIdForModel(Guest2PanelData)
force_delete = ForceDeleteForModel(Guest2PanelData)
