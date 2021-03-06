from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from iep.application.drivers.dbmodel import SqlDataModel


class PanelTimeData(SqlDataModel):
    __tablename__ = "panel_times"

    convention_uid = Column(UUID(as_uuid=True), ForeignKey("conventions.uid"))
    panel_uid = Column(UUID(as_uuid=True), ForeignKey("panels.uid"))
    room_uid = Column(UUID(as_uuid=True), ForeignKey("rooms.uid"))

    begin_date = Column(DateTime)
    end_date = Column(DateTime)

    __table_args__ = (
        UniqueConstraint("convention_uid", "panel_uid"),
        Index("convention_uid", "panel_uid"),
    )
