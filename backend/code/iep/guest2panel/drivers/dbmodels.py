from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from iep.application.drivers.dbmodel import SqlDataModel


class Guest2PanelData(SqlDataModel):
    __tablename__ = "guest2panels"

    convention_uid = Column(UUID(as_uuid=True), ForeignKey("conventions.uid"))
    guest_uid = Column(UUID(as_uuid=True), ForeignKey("guests.uid"))
    panel_uid = Column(UUID(as_uuid=True), ForeignKey("panels.uid"))
