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
    def mlist_active(self):
        with patch("iep.panels.views.list_active") as mock:
            yield mock

    @fixture
    def msave(self):
        with patch("iep.panels.views.save_new") as mock:
            yield mock

    def test_get(self, view, mlist_active):
        """
        GET should return serialized list of all active panels.
        """
        assert view.get() == mlist_active.return_value

    def test_put(self, view, msave, mrequest):
        """
        PUT should create and save new model.
        """
        mrequest.json_body = {
            'name': 'Name',
            'description': 'Description',
            'additional': 'Additional',
            'creator': 'Creator',
            'room': '101'
        }

        assert view.put() == {
            'is_success': True,
            'uid': msave.return_value
        }
