from logging import getLogger

from pyramid.httpexceptions import HTTPNotFound

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.conventions.view_mixins import BaseConventionView
from iep.guests.drivers.command import save_new
from iep.guests.drivers.command import update_by_uid
from iep.guests.drivers.query import get_active_by_uid
from iep.guests.drivers.query import list_active_by_convention
from iep.guests.schemas import GuestSchema

log = getLogger(__name__)


class GuestsView(BaseConventionView):
    def get(self):
        """
        List all active guests.
        """
        return GuestSchema(many=True).dump(
            list_active_by_convention(self._convention_uid)
        )

    def put(self):
        """
        Create new guest for logged in user.
        """
        schema = GuestSchema()
        guest = self.get_validated_fields(schema)
        guest["convention_uid"] = self._convention_uid
        uid = save_new(**guest)

        log.info("Created new Guest: {0} by {1}".format(uid, self.get_user_id()))
        log.debug("{}:{}".format(uid, guest))

        return {"is_success": True, "uid": uid}


class GuestView(BaseConventionView):
    def validate(self):
        super().validate()
        self._get_guest()

    def get(self):
        """
        Get guest data.
        """
        return GuestSchema().dump(self._get_guest())

    def patch(self):
        """
        Update guest data.
        """
        uid = self.request.matchdict["guest_uid"]
        update = self.get_validated_fields(GuestSchema())
        update_by_uid(uid, update)

        log.info("Updated Guest: {0} by {1}".format(uid, self.get_user_id()))
        log.debug("{}:{}".format(uid, update))

    @cache_per_request("guest")
    def _get_guest(self):
        try:
            return get_active_by_uid(self.request.matchdict["guest_uid"])
        except NoResultFound:
            raise HTTPNotFound()
