from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel

from .dbmodels import UserData


save_new = SaveNewForModel(UserData)
update_by_uid = UpdateByIdForModel(UserData)
delete_by_uid = DeleteByIdForModel(UserData)
force_delete = ForceDeleteForModel(UserData)

