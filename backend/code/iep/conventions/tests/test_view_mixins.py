from unittest.mock import patch

from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import ViewFixture
from iep.conventions.view_mixins import BaseConventionView


class TestBaseConventionView(ViewFixture):
    _view = BaseConventionView

    @fixture
    def mget_convention(self, view):
        with patch.object(view, "get_convention") as mock:
            yield mock

    @fixture
    def mget_active_by_uid(self):
        with patch("iep.conventions.view_mixins.get_active_by_uid") as mock:
            yield mock

    def test_validate(self, view, mget_user, mget_convention):
        """
        .validate should check if user and convention exists
        """
        view.validate()

        mget_user.assert_called_once_with()
        mget_convention.assert_called_once_with()

    def test_validate_on_error(self, view, mget_user, mget_convention):
        """
        .validate should raise HTTPNotFound when no convention found
        """
        mget_convention.side_effect = NoResultFound()

        with raises(HTTPNotFound):
            view.validate()

        mget_user.assert_called_once_with()
        mget_convention.assert_called_once_with()

    def test_get_convention(self, view, mget_active_by_uid, mrequest):
        """
        .get_convention should return convention object from convention_id in url
        """
        assert view.get_convention() == mget_active_by_uid.return_value
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["convention_id"])
