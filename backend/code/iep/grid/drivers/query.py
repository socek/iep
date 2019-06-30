from sapp import Decorator
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound

from .dbmodels import PanelTimeData
from iep import app
from iep.application.drivers.query import GetActiveByUidForModel
from iep.application.drivers.query import ListActiveForModel
from iep.application.drivers.query import NoResultFound
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
    Get active row using uniq group attributes: convention_uid, panel_uid
    """

    @Decorator(app, "dbsession")
    def _get_active(self, convention_uid, panel_uid, dbsession):
        return (
            dbsession.query(PanelTimeData, PanelData)
            .filter(
                PanelData.is_active.is_(True),
                PanelData.convention_uid == convention_uid,
                PanelTimeData.panel_uid == panel_uid,
            )
            .order_by(PanelData.created_at.desc())
            .join(PanelData)
            .one()
        )

    def __call__(self, convention_uid, panel_uid):
        try:
            panel_time, panel = self._get_active(convention_uid, panel_uid)
            data = panel_time.to_dict()
            data["panel"] = panel.to_dict()
            return data
        except (SANoResultFound, DataError):
            raise NoResultFound


class IsTimeFrameAvalible(object):
    """
    Get the time period for the panel and check if there is another item in
    that time frame.
    """

    @Decorator(app, "dbsession")
    def _get_panels_from_period(
        self, convention_uid, room_uid, begin_date, end_date, ignore_uid, dbsession
    ):
        query = (
            dbsession.query(PanelTimeData)
            .filter(
                PanelTimeData.convention_uid == convention_uid,
                PanelTimeData.room_uid == room_uid,
                or_(
                    and_(
                        PanelTimeData.begin_date > begin_date,
                        PanelTimeData.begin_date < end_date,
                    ),
                    and_(
                        PanelTimeData.end_date > begin_date,
                        PanelTimeData.end_date < end_date,
                    ),
                    and_(
                        PanelTimeData.begin_date < begin_date,
                        PanelTimeData.end_date > end_date,
                    ),
                ),
            )
        )
        if ignore_uid:
            query = query.filter(PanelTimeData.panel_uid != ignore_uid)

        return query.all()

    def __call__(self, convention_uid, room_uid, begin_date, end_date, ignore_uid=None):
        panels = self._get_panels_from_period(
            convention_uid, room_uid, begin_date, end_date, ignore_uid
        )
        return len(panels) == 0


list_active = ListActiveForModel(PanelTimeData)
get_active_by_uid = GetActiveByUidForModel(PanelTimeData)
list_active_by_convention = ListActive()
get_active = GetActive()
is_time_frame_avalible = IsTimeFrameAvalible()
