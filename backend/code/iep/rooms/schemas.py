from marshmallow.fields import String

from iep.application.schemas import DataModelSchema
from iep.application.schemas import UUID


class RoomSchema(DataModelSchema):
    name = String()
    number = String()
    floor = String()
    convention_uid = UUID()
