from logging import getLogger

from pyramid.httpexceptions import HTTPNotFound

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.conventions.view_mixins import BaseConventionView
from iep.guest2panel.drivers.command import save_new
from iep.guest2panel.drivers.command import update_by_uid
from iep.guest2panel.drivers.query import get_active_by_uid
from iep.guest2panel.drivers.query import list_active_by_convention
from iep.guest2panel.schemas import Guest2PanelSchema

log = getLogger(__name__)


class Guest2PanelsView(BaseConventionView):
    def get(self):
        """
        List all active guest2panel.
        """
        return Guest2PanelSchema(many=True).dump(
            list_active_by_convention(self._convention_uid)
        )

    def put(self):
        """
        Create new guest2panel for logged in user.
        """
        schema = Guest2PanelSchema()
        guest2panel = self.get_validated_fields(schema)
        guest2panel["convention_uid"] = self._convention_uid
        uid = save_new(**guest2panel)

        log.info("Created new Guest2Panel: {0} by {1}".format(uid, self.get_user_id()))
        log.debug("{}:{}".format(uid, guest2panel))

        return {"is_success": True, "uid": uid}


class Guest2PanelView(BaseConventionView):
    def validate(self):
        super().validate()
        self._get_guest2panel()

    def get(self):
        """
        Get guest2panel data.
        """
        return Guest2PanelSchema().dump(self._get_guest2panel())

    def patch(self):
        """
        Update guest2panel data.
        """
        uid = self.request.matchdict["guest2panel_uid"]
        update = self.get_validated_fields(Guest2PanelSchema())
        update_by_uid(uid, update)

        log.info("Updated Guest2Panel: {0} by {1}".format(uid, self.get_user_id()))
        log.debug("{}:{}".format(uid, update))

    @cache_per_request("guest2panel")
    def _get_guest2panel(self):
        try:
            return get_active_by_uid(self.request.matchdict["guest_uid"])
        except NoResultFound:
            raise HTTPNotFound()
