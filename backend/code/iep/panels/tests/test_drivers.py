from unittest.mock import patch

from pytest import fixture

from iep.application.testing import IntegrationFixture
from iep.panels.drivers import command
from iep.panels.drivers import query
from iep.panels.models import Panel


class TestPanelDrivers(IntegrationFixture):
    @fixture
    def papp(self, app):
        with patch("iep.panels.drivers.command.app", app):
            with patch("iep.panels.drivers.query.app", app):
                yield None

    def test_creating_one(self, papp):
        """
        Creating should save object and be available for listing.
        """
        uid = command.save_new(name="new name")

        assert uid
        panel = list(query.list_active())[0]
        assert panel['uid'] == uid
        assert panel['name'] == "new name"
