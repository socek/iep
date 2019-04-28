from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(object):
    _model = None
    uid = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)

    is_active = Column(Boolean, default=True, nullable=False, server_default="true")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def _update_model_after_commit(self, model):
        """
        Update uid, created_at and updated at parameters after commit. This
        are the only parameters that can change during commit.
        """
        model.uid = self.uid
        model.created_at = self.created_at
        model.updated_at = self.updated_at

    def _get_all_column_names(self):
        """
        Get all Column names declarated in the Model.
        """
        return [
            column.key for column in self.__table__.columns if column.key != "is_active"
        ]

    def to_dict(self):
        """
        Get all data from the SqlDataModel and return it in the form of dict.
        """
        data = {}
        for name in self._get_all_column_names():
            data[name] = getattr(self, name)
        return data

    def to_model(self):
        """
        Create normal model from the SqlDataModel.
        """
        return self._model(**self.to_dict())

    def from_object(self, obj):
        """
        Update SqlDataModel from normal model.
        """
        for name in self._get_all_column_names():
            value = getattr(obj, name)
            setattr(self, name, value)


SqlDataModel = declarative_base(metadata=metadata, cls=Base)
