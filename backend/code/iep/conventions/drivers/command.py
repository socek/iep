from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel

from .dbmodels import ConventionData

save_new = SaveNewForModel(ConventionData)
update_by_uid = UpdateByIdForModel(ConventionData)
delete_by_uid = DeleteByIdForModel(ConventionData)
force_delete = ForceDeleteForModel(ConventionData)
