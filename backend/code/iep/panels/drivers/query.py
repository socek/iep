from collections import defaultdict
from uuid import UUID

from sapp import Decorator
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound

from iep import app
from iep.application.drivers.query import ListActiveForModel
from iep.application.drivers.query import NoResultFound
from iep.guest2panel.drivers.dbmodels import Guest2PanelData

from .dbmodels import PanelData


class GetActiveByUidForModel(object):
    """
    Get active model from the database by uid.

    Example:
        model = get_active_by_uid(uid)
    """

    def __call__(self, uid):
        try:
            isinstance(uid, UUID) or UUID(uid)
        except (ValueError, AttributeError):
            raise NoResultFound

        [panel_data, guests_uids] = self._get_by_uid(uid)
        panel = panel_data.to_dict()
        panel["guests_uids"] = guests_uids
        return panel

    @Decorator(app, "dbsession")
    def _get_by_uid(self, uid, dbsession):
        try:
            panel_data = (
                dbsession.query(PanelData)
                .filter(PanelData.uid == uid, PanelData.is_active.is_(True))
                .one()
            )
        except (SANoResultFound, DataError):
            raise NoResultFound

        query = dbsession.query(Guest2PanelData).filter(
            Guest2PanelData.panel_uid == panel_data.uid
        )
        guests_uids = [link.guest_uid for link in query]
        return panel_data, guests_uids


class ListActiveByConventionForModel(object):
    """
    List all not delated (is_active==True) rows from the database.
    """

    @Decorator(app, "dbsession")
    def _list_active(self, convention_uid, dbsession):
        panel_data_list = (
            dbsession.query(PanelData)
            .filter(
                PanelData.is_active.is_(True),
                PanelData.convention_uid == convention_uid,
            )
            .order_by(PanelData.created_at.desc())
        )
        link_list_query = (
            dbsession.query(Guest2PanelData)
            .filter(
                PanelData.is_active.is_(True),
                PanelData.convention_uid == convention_uid,
            )
            .join(PanelData)
        )
        links = defaultdict(lambda: [])
        for link in link_list_query:
            links[link.panel_uid].append(link.guest_uid)
        for panel_data in panel_data_list:
            yield panel_data, links[panel_data.uid]

    def __call__(self, convention_uid):
        for row, guests_uids in self._list_active(convention_uid):
            rowData = row.to_dict()
            rowData["guests_uids"] = guests_uids
            yield rowData


list_active = ListActiveForModel(PanelData)
get_active_by_uid = GetActiveByUidForModel()
list_active_by_convention = ListActiveByConventionForModel()
