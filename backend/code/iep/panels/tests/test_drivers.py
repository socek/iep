from unittest.mock import patch

from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import IntegrationFixture
from iep.panels.drivers import command
from iep.panels.drivers import query
from iep.panels.models import Panel


class TestPanelDrivers(IntegrationFixture):

    @fixture
    def panel_uid(self):
        uid = command.save_new(name="new name")
        yield uid
        command.force_delete(uid)

    def test_creating_one(self, panel_uid):
        """
        Creating should save object and be available for listing.
        """
        assert panel_uid
        panel = list(query.list_active())[0]
        assert panel['uid'] == panel_uid
        assert panel['name'] == "new name"

    def test_deleting(self, panel_uid):
        """
        Delet should remove the row from normal queries.
        """
        command.delete_by_uid(panel_uid)
        assert list(query.list_active()) == []

        with raises(NoResultFound):
            query.get_active_by_uid(panel_uid)

    def test_get_active_by_uid(self):
        """
        Get By Uid should raise NoResultFound when uid is not an uuid like.
        """
        with raises(NoResultFound):
            query.get_active_by_uid(10)
