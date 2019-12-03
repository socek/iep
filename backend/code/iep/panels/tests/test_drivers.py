from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import IntegrationFixture
from iep.guest2panel.drivers.command import force_delete
from iep.guest2panel.drivers.query import list_active_by_convention
from iep.panels.drivers import command
from iep.panels.drivers import query


class TestPanelDrivers(IntegrationFixture):
    def test_creating_one(self, panel1_uid):
        """
        Creating should save object and be available for listing.
        """
        assert panel1_uid
        panel = list(query.list_active())[0]
        assert panel["uid"] == panel1_uid
        assert panel["name"] == "panel 1"

    def test_deleting(self, panel1_uid):
        """
        Delet should remove the row from normal queries.
        """
        command.delete_by_uid(panel1_uid)
        assert list(query.list_active()) == []

        with raises(NoResultFound):
            query.get_active_by_uid(panel1_uid)

    def test_get_active_by_uid(self):
        """
        Get By Uid should raise NoResultFound when uid is not an uuid like.
        """
        with raises(NoResultFound):
            query.get_active_by_uid(10)

    def test_list_active_by_conventionion(
        self, panel1_uid, panel2_1_uid, convention1_uid, convention2_uid
    ):
        """
        list_active_by_convention should return only panels in a convention
        """
        element = list(query.list_active_by_convention(convention1_uid))[0]
        assert element["uid"] == panel1_uid

    def test_create_with_guest(self, convention1_uid, guest1_uid):
        """
        .save_new will create guest link when proper guest uid provided
        """
        uid = command.save_new(
            name="panel 1",
            convention_uid=convention1_uid,
            minutes=120,
            guests_uids=[guest1_uid],
        )

        element = list(list_active_by_convention(convention1_uid))[0]
        try:
            assert element["guest_uid"] == guest1_uid
            assert element["panel_uid"] == uid
        finally:
            force_delete(element["uid"])
            command.force_delete(uid)

    def test_update_with_guest(self, convention1_uid, guest1_uid, guest2_uid):
        """
        .update_by_uid should update all fields including guests links
        """
        uid = command.save_new(
            name="panel 1",
            convention_uid=convention1_uid,
            minutes=120,
            guests_uids=[guest1_uid],
        )

        try:
            command.update_by_uid(
                uid, {"name": "Panel 1.1", "minutes": 60, "guests_uids": [guest2_uid]}
            )
            obj = query.get_active_by_uid(uid)
            assert obj["name"] == "Panel 1.1"
            assert obj["minutes"] == 60
            element = list(list_active_by_convention(convention1_uid))[0]
            assert element["panel_uid"] == uid
            assert element["guest_uid"] == guest2_uid
        finally:
            elements = list(list_active_by_convention(convention1_uid))
            for element in elements:
                force_delete(element["uid"])
            command.force_delete(uid)
