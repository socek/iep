from marshmallow.fields import DateTime
from marshmallow.fields import Nested

from iep.application.schemas import DataModelSchema
from iep.application.schemas import UUID
from iep.panels.schemas import PanelSchema


class PanelTimeSchema(DataModelSchema):

    convention_uid = UUID()
    panel_uid = UUID()
    room_uid = UUID()

    begin_date = DateTime()
    end_date = DateTime()

    panel = Nested(PanelSchema)
