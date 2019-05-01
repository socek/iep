from marshmallow import Schema
from marshmallow.fields import String
from iep.panels.models import Panel
from iep.application.schemas import ModelSchema


class PanelSchema(ModelSchema):
    MODEL = Panel

    name = String()
    description = String()
    additional = String()
    creator = String()
    room = String()


class PanelSchemaUpdate(Schema):

    name = String()
    description = String()
    additional = String()
    creator = String()
    room = String()
