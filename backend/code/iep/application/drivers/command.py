from sapp import Decorator

from iep import app


class BaseForModel(object):
    def __init__(self, model):
        self.model = model


class SaveNewForModel(BaseForModel):
    """
    Save new row's data to the database. Returns new uid of the object.

    Example:
        save_new(name="my name is", surname="slimshady")
    """

    def __call__(self, *args, **kwargs):
        obj = self.model()
        for key, value in kwargs.items():
            setattr(obj, key, value)

        uid = self._save(obj)
        return uid

    @Decorator(app, "dbsession")
    def _save(self, obj, dbsession=None):
        dbsession.add(obj)
        dbsession.commit()
        return obj.uid


class UpdateByIdForModel(BaseForModel):
    """
    Update row's data.

    Example:
        update_by_id(uid, {name:"marshal matters"})
    """

    def __call__(self, uid, update):
        update_raw = {}
        for key, value in update.items():
            update_raw[getattr(self.model, key)] = value
        self._update(uid, update_raw)

    @Decorator(app, "dbsession")
    def _update(self, uid, update, dbsession=None):
        dbsession.query(self.model).filter(self.model.uid == uid).update(update)
        dbsession.commit()


class DeleteByIdForModel(UpdateByIdForModel):
    """
    Delete (hide) the row in the database.

    Example:
        delete_by_id(uid)
    """

    def __call__(self, uid):
        super().__call__(uid, {"is_active": False})


class ForceDeleteForModel(BaseForModel):
    """
    Remove row from the database.
    !!! Use with caution !!!

    Example:
        force_delete(uid)
    """

    @Decorator(app, "dbsession")
    def __call__(self, uid, dbsession):
        dbsession.query(self.model).filter(self.model.uid == uid).delete()
        dbsession.commit()
