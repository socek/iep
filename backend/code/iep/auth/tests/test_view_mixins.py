from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import sentinel

from pyramid.httpexceptions import HTTPUnauthorized
from pytest import fixture
from pytest import raises
from sqlalchemy.orm.exc import NoResultFound
from undecorated import undecorated

from iep.application.testing import ViewFixture
from iep.auth.view_mixins import AuthMixin
from iep.auth.view_mixins import AuthenticatedView


class TestAuthMixin(object):
    @fixture
    def mixin(self):
        return AuthMixin()

    @fixture
    def mdb(self):
        return MagicMock

    @fixture
    def mquery(self):
        with patch("iep.auth.view_mixins.query") as mock:
            yield mock

    @fixture
    def mdecoded_jwt(self, mixin):
        with patch.object(mixin, "_decoded_jwt") as mock:
            mock.return_value = {"uid": sentinel.user_id}
            yield mock

    @fixture
    def mdecode_jwt(self):
        with patch("iep.auth.view_mixins.decode_jwt") as mock:
            yield mock

    @fixture
    def mrequest(self, mixin):
        mrequest = MagicMock()
        mrequest.headers = {}
        mixin.request = mrequest
        return mrequest

    @fixture
    def get_user(self, mixin):
        return undecorated(mixin.get_user)

    def test_get_user(self, mixin, mdb, mquery, get_user, mrequest, mdecoded_jwt):
        """
        .get_user should return authenticated user when proper jwt provided.
        """
        assert get_user(mixin, dbsession=mdb) == mquery.get_active_by_uid.return_value
        mquery.get_active_by_uid.assert_called_once_with(sentinel.user_id)

    def test_decoded_jwt_no_jwt_provided(self, mixin, mrequest, mdecode_jwt):
        """
        .get_user should return authenticated user when proper jwt provided.
        """
        with raises(HTTPUnauthorized):
            mixin._decoded_jwt()

    def test_decoded_jwt_proper_jwt_provided(self, mixin, mrequest, mdecode_jwt):
        """
        .get_user should return authenticated user when proper jwt provided.
        """
        mrequest.headers["JWT"] = "fake-jwt"

        assert mixin._decoded_jwt() == mdecode_jwt.return_value

        mdecode_jwt.assert_called_once_with("fake-jwt")

    def test_is_authenticated(self, mixin, mrequest):
        """
        .is_authenticated should return True only if there is jwt in headers.
        """
        assert not mixin.is_authenticated()

        mrequest.headers["JWT"] = True
        assert mixin.is_authenticated()

    def test_get_user_id(self, mixin, mdecoded_jwt):
        """
        .get_user_id should return id from jwt
        """
        mdecoded_jwt.return_value = {"uid": sentinel.user_id}

        assert mixin.get_user_id() == sentinel.user_id


class TestAuthenticatedView(ViewFixture):
    _view = AuthenticatedView

    def test_validate_when_user_found(self, view, mget_user):
        """
        .validate should do nothing, when the user is found
        """
        assert view.validate() is None

    def test_validate_when_user_not_found(self, view, mget_user):
        """
        .validate should raise HTTPUnauthorized when the user is not found
        """
        mget_user.side_effect = NoResultFound()

        with raises(HTTPUnauthorized):
            view.validate()
