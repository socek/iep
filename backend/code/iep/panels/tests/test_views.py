from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import ViewFixture
from iep.panels.views import PanelView
from iep.panels.views import PanelsView


class TestPanelsView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return PanelsView(mroot_factory, mrequest)

    @fixture
    def mlist_active_by_convention(self):
        with patch("iep.panels.views.list_active_by_convention") as mock:
            yield mock

    @fixture
    def msave(self):
        with patch("iep.panels.views.save_new") as mock:
            yield mock

    def test_get(self, view, mlist_active_by_convention, mrequest):
        """
        GET should return serialized list of all active panels.
        """
        assert view.get() == []
        mlist_active_by_convention.assert_called_once_with(mrequest.matchdict["convention_id"])

    def test_put(self, view, msave, mrequest):
        """
        PUT should create and save new model.
        """
        mrequest.json_body = {
            "name": "Name",
            "description": "Description",
            "additional": "Additional",
        }

        assert view.put() == {"is_success": True, "uid": msave.return_value}


class TestPanelView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return PanelView(mroot_factory, mrequest)

    @fixture
    def mupdate_by_uid(self):
        with patch("iep.panels.views.update_by_uid") as mock:
            yield mock

    @fixture
    def mget_active_by_uid(self):
        with patch("iep.panels.views.get_active_by_uid") as mock:
            yield mock

    @fixture
    def mget_panel(self, view):
        with patch.object(view, "_get_panel") as mock:
            yield mock

    @fixture
    def mget_user(self, view):
        with patch.object(view, "get_user") as mock:
            yield mock

    @fixture
    def mget_convention(self, view):
        with patch.object(view, "get_convention") as mock:
            yield mock

    def test_get_panel_when_not_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_panel should raise HTTPNotFound error when panel is not present.
        """
        mget_active_by_uid.side_effect = NoResultFound()
        mrequest.matchdict["panel_uid"] = uuid4().hex
        with raises(HTTPNotFound):
            view._get_panel()
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["panel_uid"])

    def test_get_panel_when_present(self, view, mrequest, mget_active_by_uid):
        """
        ._get_panel should raise HTTPNotFound error when panel is not present.
        """
        mrequest.matchdict["panel_uid"] = uuid4().hex
        assert view._get_panel() == mget_active_by_uid.return_value
        mget_active_by_uid.assert_called_once_with(mrequest.matchdict["panel_uid"])

    def test_validate(self, view, mget_panel, mget_user, mget_convention):
        """
        .validate should check if panel exists and if user is logged in
        """
        view.validate()
        mget_panel.assert_called_once_with()
        mget_user.assert_called_once_with()
        mget_convention.assert_called_once_with()

    def test_get(self, view, mget_panel):
        """
        .get should return serialized panel
        """
        uid = uuid4()
        mget_panel.return_value = {
            "uid": uid,
            "name": "my new panel",
        }

        assert view.get() == {
            "uid": uid.hex,
            "name": "my new panel",
            "guests_uids": []
        }

    def test_patch(self, view, mrequest, mupdate_by_uid):
        """
        .patch should send to database proper update data
        """
        uid = uuid4().hex
        mrequest.matchdict = {"panel_uid": uid}
        mrequest.json_body = {
            "name": "Name",
            "description": "Description",
            "additional": "Additional",
        }

        view.patch()

        mupdate_by_uid.assert_called_once_with(
            uid,
            {
                "additional": "Additional",
                "name": "Name",
                "description": "Description",
            },
        )
