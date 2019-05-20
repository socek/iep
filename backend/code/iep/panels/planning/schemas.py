from marshmallow.fields import DateTime

from iep.application.schemas import DataModelSchema
from iep.application.schemas import UUID


class PanelTimeSchema(DataModelSchema):

    convention_uid = UUID()
    panel_uid = UUID()
    room_uid = UUID()

    begin_date = DateTime()
    end_date = DateTime()
