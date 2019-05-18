from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import IntegrationFixture
from iep.panels.drivers import command
from iep.panels.drivers import query


class TestPanelDrivers(IntegrationFixture):
    @fixture
    def panel1_uid(self, convention1_uid):
        uid = command.save_new(name="new name", convention_uid=convention1_uid)
        yield uid
        command.force_delete(uid)

    @fixture
    def panel2_uid(self, convention2_uid):
        uid = command.save_new(name="new name", convention_uid=convention2_uid)
        yield uid
        command.force_delete(uid)

    def test_creating_one(self, panel1_uid):
        """
        Creating should save object and be available for listing.
        """
        assert panel1_uid
        panel = list(query.list_active())[0]
        assert panel["uid"] == panel1_uid
        assert panel["name"] == "new name"

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
        self, panel1_uid, panel2_uid, convention1_uid, convention2_uid
    ):
        """
        list_active_by_convention should return only panels in a convention
        """
        element = list(query.list_active_by_convention(convention1_uid))[0]
        assert element["uid"] == panel1_uid
