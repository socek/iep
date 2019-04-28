from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

from pytest import fixture

from iep.application.testing import ViewFixture
from iep.panels.views import PanelsView
from iep.panels.models import Panel


class TestPanelsView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return PanelsView(mroot_factory, mrequest)

    @fixture
    def mcreate_context(self):
        with patch("iep.panels.views.app.create_context") as mock:
            yield mock

    @fixture
    def mpanels_query(self):
        with patch("iep.panels.views.PanelsQuery") as mock:
            yield mock

    def test_get(self, view, mcreate_context, mpanels_query):
        """
        GET should return serialized list of all active panels.
        """
        obj = Panel(uuid4())
        mpanels_query.return_value.list_active.return_value = [obj]

        assert view.get() == [{
            "uid": obj.uid.hex,
            "name": obj.name,
            "description": obj.description,
            "additional": obj.additional,
            "creator": obj.creator,
            "room": obj.room,
        }]

        mcreate_context.assert_called_once_with()
        mpanels_query.assert_called_once_with(mcreate_context.return_value.dbsession)
