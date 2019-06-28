from datetime import timedelta
from logging import getLogger

from pyramid.httpexceptions import HTTPNotFound

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.conventions.view_mixins import BaseConventionView
from iep.panels.drivers.query import get_active_by_uid as get_panel

from iep.panels.planning.drivers.command import upsert
from iep.panels.planning.drivers.command import update_by_uid
from iep.panels.planning.drivers.query import get_active_by_uid
from iep.panels.planning.drivers.query import list_active_by_convention
from iep.panels.planning.schemas import PanelTimeSchema

log = getLogger(__name__)


class PanelTimesView(BaseConventionView):
    def get(self):
        """
        List all active panels.
        """
        return PanelTimeSchema(many=True).dump(
            list_active_by_convention(self._convention_uid)
        )

    def put(self):
        """
        Create new panel for logged in user.
        """
        schema = PanelTimeSchema()
        panel_time = self.get_validated_fields(schema)
        panel_time["convention_uid"] = self._convention_uid

        panel = get_panel(panel_time["panel_uid"])
        panel_time["end_date"] = panel_time["begin_date"] + timedelta(
            minutes=panel["minutes"]
        )

        upsert(**panel_time)

        log.info(
            "Upserted new PanelTime: Convent:{0} Panel:{1} Room:{2} by user:{3}".format(
                self._convention_uid,
                panel_time["panel_uid"],
                panel_time["room_uid"],
                self.get_user_id(),
            )
        )
        log.debug("{}".format(panel_time))

        return {"is_success": True}


class PanelTimeView(BaseConventionView):
    def validate(self):
        super().validate()
        self._get_panel_time()

    def get(self):
        """
        Get panel data.
        """
        return PanelTimeSchema().dump(self._get_panel_time())

    def patch(self):
        """
        Update panel data.
        """
        uid = self.request.matchdict["panel_uid"]
        update = self.get_validated_fields(PanelTimeSchema())
        update_by_uid(uid, update)

        log.info("Updated Panel: {0} by {1}".format(uid, self.get_user_id()))
        log.debug("{}:{}".format(uid, update))

    @cache_per_request("panel")
    def _get_panel_time(self):
        try:
            return get_active_by_uid(self.request.matchdict["panel_time_uid"])
        except NoResultFound:
            raise HTTPNotFound()
