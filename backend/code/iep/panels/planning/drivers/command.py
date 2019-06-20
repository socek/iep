from sapp import Decorator
from sqlalchemy.dialects.postgresql import insert

from iep import app
from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.application.drivers.command import UpdateByIdForModel
from iep.panels.drivers.dbmodels import PanelData


from .dbmodels import PanelTimeData


class Delete(object):
    """
    Delete PanelTimeData using uniq group attributes: convention_uid, panel_uid, room_uid
    """

    @Decorator(app, "dbsession")
    def _delete(self, convention_uid, panel_uid, room_uid, dbsession):
        [panel_time_uid] = (
            dbsession.query(PanelTimeData.uid)
            .filter(
                PanelData.is_active.is_(True),
                PanelData.convention_uid == convention_uid,
                PanelTimeData.panel_uid == panel_uid,
                PanelTimeData.room_uid == room_uid,
            )
            .join(PanelData)
            .one()
        )
        (
            dbsession.query(PanelTimeData)
            .filter(PanelTimeData.uid == panel_time_uid)
            .delete()
        )
        dbsession.commit()

    def __call__(self, convention_uid, panel_uid, room_uid):
        self._delete(convention_uid, panel_uid, room_uid)


class Upsert(object):
    """
    Insert or update PanelTimeData using uniq group attributes: convention_uid, panel_uid, room_uid
    """

    @Decorator(app, "dbsession")
    def _upsert(
        self, convention_uid, panel_uid, room_uid, begin_date, end_date, dbsession
    ):
        stament = (
            insert(PanelTimeData.__table__)
            .values(
                convention_uid=convention_uid,
                panel_uid=panel_uid,
                room_uid=room_uid,
                begin_date=begin_date,
                end_date=end_date,
            )
            .on_conflict_do_update(
                index_elements=["convention_uid", "panel_uid"],
                set_=dict(begin_date=begin_date, end_date=end_date, room_uid=room_uid),
            )
        )
        dbsession.execute(stament)
        dbsession.commit()

    def __call__(self, convention_uid, panel_uid, room_uid, begin_date, end_date):
        self._upsert(convention_uid, panel_uid, room_uid, begin_date, end_date)


save_new = SaveNewForModel(PanelTimeData)
update_by_uid = UpdateByIdForModel(PanelTimeData)
delete_by_uid = DeleteByIdForModel(PanelTimeData)
force_delete = ForceDeleteForModel(PanelTimeData)
delete = Delete()
upsert = Upsert()
