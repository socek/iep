from logging import getLogger

from pyramid.httpexceptions import HTTPNotFound

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.auth.view_mixins import AuthenticatedView
from iep.conventions.drivers.command import save_new
from iep.conventions.drivers.command import update_by_uid
from iep.conventions.drivers.query import get_active_by_uid
from iep.conventions.drivers.query import list_active
from iep.conventions.schemas import ConventionSchema

log = getLogger(__name__)


class ConventionsView(AuthenticatedView):
    def get(self):
        """
        List all active conventions.
        """
        return ConventionSchema(many=True).dump(list_active())

    def put(self):
        """
        Create new convention for logged in user.
        """
        schema = ConventionSchema()
        convention = self.get_validated_fields(schema)
        uid = save_new(**convention)

        log.info("Created new Convention: {0} by {1}".format(uid, self.get_user_id()))
        log.debug("{}:{}".format(uid, convention))

        return {"is_success": True, "uid": uid}


class ConventionView(AuthenticatedView):
    def validate(self):
        super().validate()
        self._get_convention()

    def get(self):
        """
        Get convention data.
        """
        return ConventionSchema().dump(self._get_convention())

    def patch(self):
        """
        Update convention data.
        """
        uid = self.request.matchdict["convention_uid"]
        update = self.get_validated_fields(ConventionSchema())
        update_by_uid(uid, update)

        log.info("Updated Convention: {0} by {1}".format(uid, self.get_user_id()))
        log.debug("{}:{}".format(uid, update))

    @cache_per_request("convention")
    def _get_convention(self):
        try:
            return get_active_by_uid(self.request.matchdict["convention_uid"])
        except NoResultFound:
            raise HTTPNotFound()
