from sqlalchemy import Binary
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from iep.application.drivers.dbmodel import SqlDataModel
from iep.panels.models import Panel


class PanelData(SqlDataModel):
    __tablename__ = "panels"
    _model = Panel

    name = Column(String, nullable=True)
    description = Column(String)
    additional = Column(String)
    creator = Column(String)

