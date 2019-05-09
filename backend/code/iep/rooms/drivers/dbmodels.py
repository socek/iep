from sqlalchemy import Column
from sqlalchemy import String

from iep.application.drivers.dbmodel import SqlDataModel


class RoomData(SqlDataModel):
    __tablename__ = "rooms"

    name = Column(String)
    number = Column(String)
    floor = Column(String)
