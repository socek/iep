from sqlalchemy import Binary
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from iep.application.drivers.dbmodel import SqlDataModel
from iep.auth.models import User


class UserData(SqlDataModel):
    __tablename__ = "users"
    _model = User

    name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    password = Column(Binary(100), nullable=True)
