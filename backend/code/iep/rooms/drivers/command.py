from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel

from .dbmodels import RoomData

save_new = SaveNewForModel(RoomData)
update_by_uid = UpdateByIdForModel(RoomData)
delete_by_uid = DeleteByIdForModel(RoomData)
force_delete = ForceDeleteForModel(RoomData)
