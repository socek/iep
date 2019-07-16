from marshmallow.fields import String

from iep.application.schemas import DataModelSchema
from iep.application.schemas import UUID


class GuestSchema(DataModelSchema):
    convention_uid = UUID()
    name = String()
    kind = String()
    description = String()
