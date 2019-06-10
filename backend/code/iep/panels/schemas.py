from marshmallow.fields import Boolean
from marshmallow.fields import Integer
from marshmallow.fields import String

from iep.application.schemas import DataModelSchema
from iep.application.schemas import UUID


class PanelSchema(DataModelSchema):

    convention_uid = UUID()
    name = String()
    description = String()
    additional = String()
    creator = String()
    room = String()
    accepted = Boolean()
    minutes = Integer()
