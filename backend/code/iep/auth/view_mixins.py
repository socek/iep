from pyramid.httpexceptions import HTTPUnauthorized
from sapp import Decorator
from sqlalchemy.orm.exc import NoResultFound

from iep import app
from iep.application.cache import cache_per_request
from iep.application.views import RestfulView
from iep.auth.drivers import query
from iep.auth.jwt import decode_jwt


class AuthMixin(object):
    @cache_per_request("user")
    @Decorator(app, "dbsession")
    def get_user(self, dbsession):
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
