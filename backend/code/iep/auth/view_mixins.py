from pyramid.httpexceptions import HTTPUnauthorized

from iep.application.cache import cache_per_request
from iep.application.drivers.query import NoResultFound
from iep.application.views import RestfulView
from iep.auth.drivers import query
from iep.auth.jwt import decode_jwt


class AuthMixin(object):
    @cache_per_request("user")
    def get_user(self):
        """
        Get current logged in user depending on the JWT token.
        """
        payload = self._decoded_jwt()
        return query.get_active_by_uid(payload["uid"])

    def is_authenticated(self):
        return self.request.headers.get("JWT") is not None

    def get_user_id(self):
        return self._decoded_jwt()["uid"]

    def _decoded_jwt(self):
        jwt = self.request.headers.get("JWT")
        if jwt:
            return decode_jwt(jwt)
        else:
            raise HTTPUnauthorized()


class AuthenticatedView(RestfulView, AuthMixin):
    def validate(self):
        try:
            self.get_user()
        except NoResultFound:
            raise HTTPUnauthorized()
