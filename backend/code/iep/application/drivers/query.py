from uuid import UUID

from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound

from iep import app
from iep.application.app import Decorator


class NoResultFound(Exception):
    pass


class BaseForModel(object):
    def __init__(self, model):
        self.model = model


class GetActiveByUidForModel(BaseForModel):
    """
    Get active model from the database by uid.

    Example:
        model = get_by_id(uid)
    """

    def __call__(self, uid):
        try:
            isinstance(uid, UUID) or UUID(uid)
        except (ValueError, AttributeError):
            raise NoResultFound

        return self._get_by_uid(uid).to_model()

    @Decorator(app, "dbsession")
    def _get_by_uid(self, uid, dbsession):
        try:
            return (
                dbsession.query(self.model)
                .filter(self.model.uid == uid, self.model.is_active.is_(True))
                .one()
            )
        except (SANoResultFound, DataError):
            raise NoResultFound


class ListActiveForModel(BaseForModel):
    """
    List all not delated (is_active==True) rows from the database.
    """
    @Decorator(app, "dbsession")
    def _list_active(self, dbsession):
        return dbsession.query(self.model).filter(self.model.is_active.is_(True))

    def __call__(self):
        for row in self._list_active():
            yield row.to_dict()
