from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import ViewFixture
from iep.guests.views import GuestView
from iep.guests.views import GuestsView


class TestGuestsView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return GuestsView(mroot_factory, mrequest)

    @fixture
    def mlist_active_by_convention(self):
        with patch("iep.guests.views.list_active_by_convention") as mock:
            yield mock

    @fixture
    def msave(self):
        with patch("iep.guests.views.save_new") as mock:
            yield mock

    def test_get(self, view, mlist_active_by_convention, mrequest):
        """
        GET should return serialized list of all active guests.
        """
        assert view.get() == []
        mlist_active_by_convention.assert_called_once_with(mrequest.matchdict["convention_id"])

    def test_put(self, view, msave, mrequest):
        """
        PUT should create and save new model.
        """
        mrequest.json_body = {
            "name": "Name",
            "kind": "vip",
            "description": "Description",
        }

        assert view.put() == {"is_success": True, "uid": msave.return_value}


class TestGuestView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return GuestView(mroot_factory, mrequest)

    @fixture
    def mupdate_by_uid(self):
        with patch("iep.guests.views.update_by_uid") as mock:
            yield mock

    @fixture
    def mget_active_by_uid(self):
        with patch("iep.guests.views.get_active_by_uid") as mock:
            yield mock

    @fixture
    def mget_guest(self, view):
        with patch.object(view, "_get_guest") as mock:
            yield mock

    @fixture
    def mget_user(self, view):
        with patch.object(view, "get_user") as mock:
            yield mock

    @fixture
    def mget_convention(self, view):
        with patch.object(view, "get_convention") as mock:
            yield mock

    def test_get_guest_when_not_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_guest should raise HTTPNotFound error when guest is not present.
        """
        mget_active_by_uid.side_effect = NoResultFound()
        mrequest.matchdict["guest_uid"] = uuid4().hex
        with raises(HTTPNotFound):
            view._get_guest()
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["guest_uid"])

    def test_get_guest_when_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_guest should raise HTTPNotFound error when guest is not present.
        """
        mrequest.matchdict["guest_uid"] = uuid4().hex
        assert view._get_guest() == mget_active_by_uid.return_value
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["guest_uid"])

    def test_validate(self, view, mget_guest, mget_user, mget_convention):
        """
        .validate should check if guest exists and if user is logged in
        """
        view.validate()
        mget_guest.assert_called_once_with()
        mget_user.assert_called_once_with()
        mget_convention.assert_called_once_with()

    def test_get(self, view, mget_guest):
        """
        .get should return serialized guest
        """
        uid = uuid4()
        mget_guest.return_value = {
            "uid": uid,
            "name": "my new guest",
        }

        assert view.get() == {
            "uid": uid.hex,
            "name": "my new guest",
        }

    def test_patch(self, view, mrequest, mupdate_by_uid):
        """
        .patch should send to database proper update data
        """
        uid = uuid4().hex
        mrequest.matchdict = {"guest_uid": uid}
        mrequest.json_body = {
            "name": "Name",
            "kind": "vip",
            "description": "Description",
        }

        view.patch()

        mupdate_by_uid.assert_called_once_with(
            uid,
            {
                "name": "Name",
                "kind": "vip",
                "description": "Description",
            },
        )
