from iep.application.schemas import DataModelSchema
from iep.application.schemas import UUID


class Guest2PanelSchema(DataModelSchema):
    convention_uid = UUID()
    guest_uid = UUID()
    panel_uid = UUID()
