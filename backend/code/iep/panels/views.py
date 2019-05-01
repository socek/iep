from logging import getLogger

from pyramid.httpexceptions import HTTPNotFound

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.application.views import RestfulView
from iep.panels.drivers.command import save_new
from iep.panels.drivers.command import update_by_uid
from iep.panels.drivers.query import get_active_by_uid
from iep.panels.drivers.query import list_active
from iep.panels.schemas import PanelSchema
from iep.panels.schemas import PanelSchemaUpdate

log = getLogger(__name__)


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
        uid = save_new(**panel.to_dict())

        log.info("Created new Panel: {0}".format(uid))
        log.debug("{}:{}".format(uid, panel.to_dict()))

        return {"is_success": True, "uid": uid}


class PanelView(RestfulView):
    def validate(self):
        self._get_panel()

    def get(self):
        """
        Get panel data.
        """
        return PanelSchema().dump(self._get_panel())

    def patch(self):
        """
        Update panel data.
        """
        uid = self.request.matchdict["panel_uid"]
        update = self.get_validated_fields(PanelSchemaUpdate(), partial=("uid",))
        update_by_uid(uid, update)

        log.info("Updated Panel: {0}".format(uid))
        log.debug("{}:{}".format(uid, update))

    @cache_per_request("panel")
    def _get_panel(self):
        try:
            return get_active_by_uid(self.request.matchdict["panel_uid"])
        except NoResultFound:
            raise HTTPNotFound()
