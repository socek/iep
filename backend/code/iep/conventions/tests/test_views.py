from datetime import datetime
from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import ViewFixture
from iep.conventions.views import ConventionView
from iep.conventions.views import ConventionsView


class TestConventionsView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return ConventionsView(mroot_factory, mrequest)

    @fixture
    def mlist_active(self):
        with patch("iep.conventions.views.list_active") as mock:
            yield mock

    @fixture
    def msave(self):
        with patch("iep.conventions.views.save_new") as mock:
            yield mock

    def test_get(self, view, mlist_active):
        """
        GET should return serialized list of all active conventions.
        """
        assert view.get() == []
        mlist_active.assert_called_once_with()

    def test_put(self, view, msave, mrequest):
        """
        PUT should create and save new model.
        """
        mrequest.json_body = {
            "name": "Name",
            "start_date": "2018-10-10 10:00:00",
            "end_date": "2018-10-12 10:00:00",
        }

        assert view.put() == {"is_success": True, "uid": msave.return_value}


class TestConventionView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return ConventionView(mroot_factory, mrequest)

    @fixture
    def mupdate_by_uid(self):
        with patch("iep.conventions.views.update_by_uid") as mock:
            yield mock

    @fixture
    def mget_active_by_uid(self):
        with patch("iep.conventions.views.get_active_by_uid") as mock:
            yield mock

    @fixture
    def mget_convention(self, view):
        with patch.object(view, "_get_convention") as mock:
            yield mock

    @fixture
    def mget_user(self, view):
        with patch.object(view, "get_user") as mock:
            yield mock

    def test_get_convention_when_not_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_convention should raise HTTPNotFound error when convention is not present.
        """
        mget_active_by_uid.side_effect = NoResultFound()
        mrequest.matchdict["convention_uid"] = uuid4().hex
        with raises(HTTPNotFound):
            view._get_convention()
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["convention_uid"])

    def test_get_convention_when_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_convention should raise HTTPNotFound error when convention is not present.
        """
        mrequest.matchdict["convention_uid"] = uuid4().hex
        assert view._get_convention() == mget_active_by_uid.return_value
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["convention_uid"])

    def test_validate(self, view, mget_convention, mget_user):
        """
        .validate should check if convention exists and if user is logged in
        """
        view.validate()
        mget_convention.assert_called_once_with()
        mget_user.assert_called_once_with()

    def test_get(self, view, mget_convention):
        """
        .get should return serialized convention
        """
        uid = uuid4()
        mget_convention.return_value = {
            "uid": uid,
            "name": "my new convention",
            "start_date": datetime(2018, 10, 10, 10, 0),
            "end_date": datetime(2018, 10, 12, 10, 0),
        }

        assert view.get() == {
            "uid": uid.hex,
            "name": "my new convention",
            "start_date": "2018-10-10T10:00:00",
            "end_date": "2018-10-12T10:00:00",
        }

    def test_patch(self, view, mrequest, mupdate_by_uid):
        """
        .patch should send to database proper update data
        """
        uid = uuid4().hex
        mrequest.matchdict = {"convention_uid": uid}
        mrequest.json_body = {
            "name": "Name",
            "start_date": "2018-10-10 10:00:00",
            "end_date": "2018-10-12 10:00:00",
        }

        view.patch()

        mupdate_by_uid.assert_called_once_with(
            uid,
            {
                "name": "Name",
                "start_date": datetime(2018, 10, 10, 10, 0),
                "end_date": datetime(2018, 10, 12, 10, 0),
            },
        )
