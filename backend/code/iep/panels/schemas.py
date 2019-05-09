from marshmallow import Schema
from marshmallow.fields import Boolean
from marshmallow.fields import String

from iep.application.schemas import ModelSchema
from iep.panels.models import Panel


class PanelSchema(ModelSchema):
    MODEL = Panel

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
