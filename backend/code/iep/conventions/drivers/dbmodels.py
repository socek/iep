from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

from iep.application.drivers.dbmodel import SqlDataModel


class ConventionData(SqlDataModel):
    __tablename__ = "conventions"

    name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
