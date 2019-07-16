from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from iep.application.drivers.dbmodel import SqlDataModel


class GuestData(SqlDataModel):
    __tablename__ = "guests"

    convention_uid = Column(UUID(as_uuid=True), ForeignKey("conventions.uid"))
    name = Column(String)
    kind = Column(String)
    description = Column(String)
