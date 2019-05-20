from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from iep.application.drivers.dbmodel import SqlDataModel


class PanelData(SqlDataModel):
    __tablename__ = "panels"

    convention_uid = Column(UUID(as_uuid=True), ForeignKey('conventions.uid'))
    name = Column(String, nullable=True)
    description = Column(String)
    additional = Column(String)
    creator = Column(String)
    room = Column(String)
    accepted = Column(Boolean, default=False)
