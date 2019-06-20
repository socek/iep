from sapp import Decorator

from .dbmodels import PanelTimeData
from iep import app
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel
from iep.panels.drivers.dbmodels import PanelData


class ListActive(object):
    """
    List all active rows.
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
            data["panel"] = panel.to_dict()
            yield data


class GetActive(object):
    """
    Get active row using uniq group attributes: convention_uid, panel_uid, room_uid
    """
    @Decorator(app, "dbsession")
    def _get_active(self, convention_uid, panel_uid, room_uid, dbsession):
        return (
            dbsession.query(PanelTimeData, PanelData)
            .filter(
                PanelData.is_active.is_(True),
                PanelData.convention_uid == convention_uid,
                PanelTimeData.panel_uid == panel_uid,
                PanelTimeData.room_uid == room_uid,
            )
            .order_by(PanelData.created_at.desc())
            .join(PanelData)
            .one()
        )

    def __call__(self, convention_uid, panel_uid, room_uid):
        panel_time, panel = self._get_active(convention_uid, panel_uid, room_uid)
        data = panel_time.to_dict()
        data["panel"] = panel.to_dict()
        return data


list_active = ListActiveForModel(PanelTimeData)
get_active_by_uid = GetActiveByUidForModel(PanelTimeData)
list_active_by_convention = ListActive()
get_active = GetActive()
