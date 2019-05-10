from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import ViewFixture
from iep.rooms.views import RoomView
from iep.rooms.views import RoomsView


class TestRoomsView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return RoomsView(mroot_factory, mrequest)

    @fixture
    def mlist_active(self):
        with patch("iep.rooms.views.list_active") as mock:
            yield mock

    @fixture
    def msave(self):
        with patch("iep.rooms.views.save_new") as mock:
            yield mock

    def test_get(self, view, mlist_active):
        """
        GET should return serialized list of all active rooms.
        """
        assert view.get() == []
        mlist_active.assert_called_once_with()

    def test_put(self, view, msave, mrequest):
        """
        PUT should create and save new model.
        """
        mrequest.json_body = {
            "name": "Name",
            "number": "Description",
            "floor": "Additional",
        }

        assert view.put() == {"is_success": True, "uid": msave.return_value}


class TestRoomView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return RoomView(mroot_factory, mrequest)

    @fixture
    def mupdate_by_uid(self):
        with patch("iep.rooms.views.update_by_uid") as mock:
            yield mock

    @fixture
    def mget_active_by_uid(self):
        with patch("iep.rooms.views.get_active_by_uid") as mock:
            yield mock

    @fixture
    def mget_room(self, view):
        with patch.object(view, "_get_room") as mock:
            yield mock

    @fixture
    def mget_user(self, view):
        with patch.object(view, "get_user") as mock:
            yield mock

    def test_get_room_when_not_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_room should raise HTTPNotFound error when room is not present.
        """
        mget_active_by_uid.side_effect = NoResultFound()
        mrequest.matchdict["room_uid"] = uuid4().hex
        with raises(HTTPNotFound):
            view._get_room()
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["room_uid"])

    def test_get_room_when_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_room should raise HTTPNotFound error when room is not present.
        """
        mrequest.matchdict["room_uid"] = uuid4().hex
        assert view._get_room() == mget_active_by_uid.return_value
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["room_uid"])

    def test_validate(self, view, mget_room, mget_user):
        """
        .validate should check if room exists and if user is logged in
        """
        view.validate()
        mget_room.assert_called_once_with()
        mget_user.assert_called_once_with()

    def test_get(self, view, mget_room):
        """
        .get should return serialized room
        """
        uid = uuid4()
        mget_room.return_value = {"uid": uid, "name": "my new room"}

        assert view.get() == {
            "uid": uid.hex,
            "name": "my new room",
        }

    def test_patch(self, view, mrequest, mupdate_by_uid):
        """
        .patch should send to database proper update data
        """
        uid = uuid4().hex
        mrequest.matchdict = {"room_uid": uid}
        mrequest.json_body = {
            "name": "Name",
            "number": "Description",
            "floor": "Additional",
        }

        view.patch()

        mupdate_by_uid.assert_called_once_with(
            uid,
            {
                "floor": "Additional",
                "name": "Name",
                "number": "Description",
            },
        )
