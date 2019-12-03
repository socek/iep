from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import IntegrationFixture
from iep.rooms.drivers import command
from iep.rooms.drivers import query


class TestRoomDrivers(IntegrationFixture):
    def test_creating_one(self, room1_uid):
        """
        Creating should save object and be available for listing.
        """
        assert room1_uid
        panel = list(query.list_active())[0]
        assert panel["uid"] == room1_uid
        assert panel["name"] == "room 1"

    def test_deleting(self, room1_uid):
        """
        Delet should remove the row from normal queries.
        """
        command.delete_by_uid(room1_uid)
        assert list(query.list_active()) == []

        with raises(NoResultFound):
            query.get_active_by_uid(room1_uid)

    def test_get_active_by_uid(self):
        """
        Get By Uid should raise NoResultFound when uid is not an uuid like.
        """
        with raises(NoResultFound):
            query.get_active_by_uid(10)

    def test_list_active_by_conventionion(
        self, room1_uid, room2_1_uid, convention1_uid, convention2_uid
    ):
        """
        list_active_by_convention should return only rooms in a convention
        """
        element = list(query.list_active_by_convention(convention1_uid))[0]
        assert element["uid"] == room1_uid
