from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from iep.application.drivers.dbmodel import SqlDataModel


class RoomData(SqlDataModel):
    __tablename__ = "rooms"

    convention_uid = Column(UUID(as_uuid=True), ForeignKey('conventions.uid'))
    name = Column(String)
    number = Column(String)
    floor = Column(String)
