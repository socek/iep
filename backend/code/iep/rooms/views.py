from logging import getLogger

from pyramid.httpexceptions import HTTPNotFound

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.auth.view_mixins import AuthenticatedView
from iep.rooms.drivers.command import save_new
from iep.rooms.drivers.command import update_by_uid
from iep.rooms.drivers.query import get_active_by_uid
from iep.rooms.drivers.query import list_active
from iep.rooms.schemas import RoomSchema

log = getLogger(__name__)


class RoomsView(AuthenticatedView):
    def get(self):
        """
        List all active rooms.
        """
        return RoomSchema(many=True).dump(list_active())

    def put(self):
        """
        Create new room for logged in user.
        """
        schema = RoomSchema()
        room = self.get_validated_fields(schema, partial=("uid",))
        uid = save_new(**room)

        log.info("Created new Room: {0}".format(uid))
        log.debug("{}:{}".format(uid, room))

        return {"is_success": True, "uid": uid}


class RoomView(AuthenticatedView):
    def validate(self):
        super().validate()
        self._get_room()

    def get(self):
        """
        Get room data.
        """
        return RoomSchema().dump(self._get_room())

    def patch(self):
        """
        Update room data.
        """
        uid = self.request.matchdict["room_uid"]
        update = self.get_validated_fields(RoomSchema(), partial=("uid",))
        update_by_uid(uid, update)

        log.info("Updated Room: {0}".format(uid))
        log.debug("{}:{}".format(uid, update))

    @cache_per_request("room")
    def _get_room(self):
        try:
            return get_active_by_uid(self.request.matchdict["room_uid"])
        except NoResultFound:
            raise HTTPNotFound()
