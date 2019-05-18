from marshmallow import Schema
from marshmallow.fields import Boolean
from marshmallow.fields import String

from iep.application.schemas import ModelSchema
from iep.panels.models import Panel
from iep.application.schemas import UUID


class PanelSchema(ModelSchema):
    MODEL = Panel

    convention_uid = UUID()
    name = String()
    description = String()
    additional = String()
    creator = String()
    room = String()
    accepted = Boolean()


class PanelSchemaUpdate(Schema):

    name = String()
    description = String()
    additional = String()
    creator = String()
    room = String()
    accepted = Boolean()
