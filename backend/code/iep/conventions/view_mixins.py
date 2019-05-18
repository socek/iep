from pyramid.httpexceptions import HTTPNotFound

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.auth.view_mixins import AuthenticatedView
from iep.conventions.drivers.query import get_active_by_uid


class BaseConventionView(AuthenticatedView):
    @property
    def _convention_uid(self):
        return self.request.matchdict["convention_uid"]

    @cache_per_request("convention")
    def get_convention(self):
        return get_active_by_uid(self._convention_uid)

    def validate(self):
        super().validate()
        try:
            self.get_convention()
        except NoResultFound:
            raise HTTPNotFound()
