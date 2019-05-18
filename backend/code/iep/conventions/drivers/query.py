from sapp import Decorator

from iep import app
from iep.application.drivers.query import BaseForModel
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel

from .dbmodels import ConventionData

list_active = ListActiveForModel(ConventionData)
get_active_by_uid = GetActiveByUidForModel(ConventionData)


class ListActiveByConventionForModel(BaseForModel):
    """
    List all not delated (is_active==True) rows from the database.
    """

    @Decorator(app, "dbsession")
    def _list_active(self, convention_uid, dbsession):
        return (
            dbsession.query(self.model)
            .filter(
                self.model.is_active.is_(True),
                self.model.convention_uid == convention_uid,
            )
            .order_by(self.model.created_at.desc())
        )

    def __call__(self, convention_uid):
        for row in self._list_active(convention_uid):
            yield row.to_dict()
