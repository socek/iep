from marshmallow.fields import Date
from marshmallow.fields import Decimal
from marshmallow.fields import Nested
from marshmallow.fields import String
from marshmallow.fields import UUID

from iep.application.schemas import ModelSchema
from iep.panels.models import Panel


class PanelSchema(ModelSchema):
    MODEL = Panel

    name = String()
    description = String()
    additional = String()
    creator = String()
    room = String()
