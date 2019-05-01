from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest

from iep import app
from iep.application.app import ContextManager
from iep.application.cache import cache_per_request
from iep.application.views import RestfulView
from iep.panels.drivers.command import save_new
from iep.panels.drivers.command import update_by_uid
from iep.panels.drivers.query import list_active
from iep.panels.schemas import PanelSchema


class PanelsView(RestfulView):
    def get(self):
        """
        List all active panels.
        """
        return list_active()

    def put(self):
        """
        Create new panel for logged in user.
        """
        schema = PanelSchema()
        panel = self.get_validated_fields(schema, partial=("uid",))
        uid = save_new(panel)
        return {"is_success": True, "uid": uid}


class PanelView(RestfulView):
    def validate(self):
        self._get_panel()

    def get(self):
        """
        Get panel data.
        """
        schema = PanelSchema()
        return schema.dump(self._get_panel())

    def patch(self):
        """
        Update panel data.
        """
        uid = self.request.matchdict["panel_uid"]
        update = self.get_validated_fields(PanelSchema(), partial=("uid"))
        update_by_uid(uid, update)

    @cache_per_request("panel")
    def _get_panel(self):
        try:
            return self.panel_query().get_active_by_uid(
                self.request.matchdict["panel_uid"],
                self.request.matchdict["wallet_uid"],
                True,
            )
        except NoResultFound:
            raise HTTPNotFound()
