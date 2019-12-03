from sapp import Decorator

from iep import app
from iep.application.drivers.command import DeleteByIdForModel
from iep.application.drivers.command import ForceDeleteForModel
from iep.application.drivers.command import SaveNewForModel
from iep.guest2panel.drivers.dbmodels import Guest2PanelData

from .dbmodels import PanelData


class SaveNewForModel(SaveNewForModel):
    """
    Save new row's data to the database. Returns new uid of the object.

    Example:
        save_new(name="my name is", surname="slimshady")
    """

    def __init__(self):
        super().__init__(PanelData)

    def __call__(self, *args, **kwargs):
        guests_uids = kwargs.pop("guests_uids", [])
        obj = self._set_kwargs_in_obj(kwargs)
        uid = self._save(obj, guests_uids)
        return uid

    @Decorator(app, "dbsession")
    def _save(self, obj, guests_uids, dbsession):
        dbsession.add(obj)
        dbsession.flush()

        for guest_uid in guests_uids:
            link = Guest2PanelData()
            link.convention_uid = obj.convention_uid
            link.panel_uid = obj.uid
            link.guest_uid = guest_uid
            dbsession.add(link)

        dbsession.commit()
        return obj.uid


class UpdateByIdForModel(object):
    """
    Update row's data.

    Example:
        update_by_id(uid, {name:"marshal matters"})
    """

    def __call__(self, uid, update):
        guests_uids = update.pop("guests_uids", [])
        update_raw = {}
        for key, value in update.items():
            update_raw[getattr(PanelData, key)] = value
        self._update(uid, update_raw, guests_uids)

    @Decorator(app, "dbsession")
    def _update(self, uid, update, guests_uids, dbsession=None):
        dbsession.query(PanelData).filter(PanelData.uid == uid).update(update)
        convention_uid = (
            dbsession.query(PanelData).filter(PanelData.uid == uid).one().convention_uid
        )

        old_links = (
            dbsession.query(Guest2PanelData)
            .filter(Guest2PanelData.panel_uid == uid)
            .all()
        )

        # Remove old
        guests_to_remove = [
            link.uid for link in old_links if link.guest_uid not in guests_uids
        ]
        dbsession.query(Guest2PanelData).filter(
            Guest2PanelData.uid.in_(guests_to_remove)
        ).delete(synchronize_session=False)

        # Create missing
        guests_already_added = [link.guest_uid for link in old_links]
        guests_to_add = [
            guest_uid
            for guest_uid in guests_uids
            if guest_uid not in guests_already_added
        ]
        for guest_uid in guests_to_add:
            link = Guest2PanelData()
            link.convention_uid = convention_uid
            link.panel_uid = uid
            link.guest_uid = guest_uid
            dbsession.add(link)

        dbsession.commit()


class ForceDeleteForPanel(ForceDeleteForModel):
    def __init__(self):
        self.model = PanelData

    @Decorator(app, "dbsession")
    def __call__(self, uid, dbsession):
        dbsession.query(Guest2PanelData).filter(Guest2PanelData.panel_uid == uid).delete()
        dbsession.query(self.model).filter(self.model.uid == uid).delete()
        dbsession.commit()


save_new = SaveNewForModel()
update_by_uid = UpdateByIdForModel()
delete_by_uid = DeleteByIdForModel(PanelData)
force_delete = ForceDeleteForPanel()
