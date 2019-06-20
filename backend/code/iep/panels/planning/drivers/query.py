from sapp import Decorator

from .dbmodels import PanelTimeData
from iep import app
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel
from iep.panels.drivers.dbmodels import PanelData


class ListActive(object):
    """
    List all not delated (is_active==True) rows from the database.
    """

    @Decorator(app, "dbsession")
    def _list_active(self, convention_uid, dbsession):
        return (
            dbsession.query(PanelTimeData, PanelData)
            .filter(
                PanelData.is_active.is_(True),
                PanelData.convention_uid == convention_uid,
            )
            .order_by(PanelData.created_at.desc())
            .join(PanelData)
        )

    def __call__(self, convention_uid):
        for panel_time, panel in self._list_active(convention_uid):
            data = panel_time.to_dict()
            data['panel'] = panel.to_dict()
            yield data


list_active = ListActiveForModel(PanelTimeData)
get_active_by_uid = GetActiveByUidForModel(PanelTimeData)
list_active_by_convention = ListActive()
