from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel

from .dbmodels import GuestData

save_new = SaveNewForModel(GuestData)
update_by_uid = UpdateByIdForModel(GuestData)
delete_by_uid = DeleteByIdForModel(GuestData)
force_delete = ForceDeleteForModel(GuestData)
