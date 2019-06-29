# from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import IntegrationFixture
from iep.grid.drivers.command import delete
from iep.grid.drivers.command import save_new
from iep.grid.drivers.command import upsert
from iep.grid.drivers.query import get_active
from iep.grid.drivers.query import get_active_by_uid
from iep.grid.drivers.query import list_active_by_convention


class TestPanelTimeDelete(IntegrationFixture):
    def test_deleting(self, convention1_uid, panel1_uid, room1_uid):
        """
        delete should delete the object from the database
        """
        uid = save_new(
            convention_uid=convention1_uid, panel_uid=panel1_uid, room_uid=room1_uid
        )

        delete(convention_uid=convention1_uid, panel_uid=panel1_uid)

        with raises(NoResultFound):
            get_active_by_uid(uid)

    def test_upsert_new(self, convention1_uid, panel1_uid, room1_uid):
        """
        upsert should create new object when non is created
        """

        upsert(convention1_uid, panel1_uid, room1_uid, None, None)

        try:
            obj = get_active(convention1_uid, panel1_uid)
            assert obj["room_uid"] == room1_uid
        finally:
            delete(convention1_uid, panel1_uid)

    def test_upsert_old(self, convention1_uid, panel1_uid, room1_uid, room2_uid):
        """
        upsert should update object when there is one already
        """

        upsert(convention1_uid, panel1_uid, room1_uid, None, None)
        upsert(convention1_uid, panel1_uid, room2_uid, None, None)

        try:
            obj = get_active(convention1_uid, panel1_uid)
            assert obj["room_uid"] == room2_uid
        finally:
            delete(convention1_uid, panel1_uid)

    def test_list_active_by_convention(
        self, convention1_uid, convention2_uid, paneltime1_uid
    ):
        """
        list_active_by_convention should list only elements for specyfied convention
        """
        elements = list(list_active_by_convention(convention1_uid))
        assert len(elements) == 1
        assert elements[0]["uid"] == paneltime1_uid

        elements = list(list_active_by_convention(convention2_uid))
        assert len(elements) == 0
