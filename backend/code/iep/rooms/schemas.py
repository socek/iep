from marshmallow.fields import String

from iep.application.schemas import DataModelSchema


class RoomSchema(DataModelSchema):
    name = String()
    number = String()
    floor = String()
