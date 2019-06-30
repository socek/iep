from datetime import datetime
from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPConflict
from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import ViewFixture
from iep.grid.views import PanelTimeView
from iep.grid.views import PanelTimesView


class TestPanelTimesView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return PanelTimesView(mroot_factory, mrequest)

    @fixture
    def mlist_active_by_convention(self):
        with patch("iep.grid.views.list_active_by_convention") as mock:
            yield mock

    @fixture
    def mupsert(self):
        with patch("iep.grid.views.upsert") as mock:
            yield mock

    @fixture
    def mget_panel(self):
        with patch("iep.grid.views.get_panel") as mock:
            yield mock

    @fixture
    def mis_time_frame_avalible(self):
        with patch("iep.grid.views.is_time_frame_avalible") as mock:
            yield mock

    def test_get(self, view, mlist_active_by_convention, mrequest):
        """
        GET should return serialized list of all active panels.
        """
        assert view.get() == []
        mlist_active_by_convention.assert_called_once_with(
            mrequest.matchdict["convention_id"]
        )

    def test_put(self, view, mupsert, mget_panel, mrequest, mis_time_frame_avalible):
        """
        PUT should create and save new model.
        """
        mis_time_frame_avalible.return_value = True
        mrequest.json_body = {
            "convention_uid": uuid4().hex,
            "panel_uid": uuid4().hex,
            "room_uid": uuid4().hex,
            "begin_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat(),
        }

        mget_panel.return_value = {"minutes": 15}

        assert view.put() == {"is_success": True}

    def test_put_on_conflict(self, view, mupsert, mget_panel, mrequest, mis_time_frame_avalible):
        """
        PUT should raise error when time frame is already taken
        """
        mis_time_frame_avalible.return_value = False
        mrequest.json_body = {
            "convention_uid": uuid4().hex,
            "panel_uid": uuid4().hex,
            "room_uid": uuid4().hex,
            "begin_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat(),
        }

        mget_panel.return_value = {"minutes": 15}

        with raises(HTTPConflict):
            view.put()


class TestPanelTimeView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return PanelTimeView(mroot_factory, mrequest)

    @fixture
    def mupdate_by_uid(self):
        with patch("iep.grid.views.update_by_uid") as mock:
            yield mock

    @fixture
    def mget_active(self):
        with patch("iep.grid.views.get_active") as mock:
            yield mock

    @fixture
    def mget_panel(self, view):
        with patch("iep.grid.views.get_panel") as mock:
            yield mock

    @fixture
    def mdelete(self, view):
        with patch("iep.grid.views.delete") as mock:
            yield mock

    @fixture
    def mget_panel_time(self, view):
        with patch.object(view, "_get_panel_time") as mock:
            yield mock

    @fixture
    def mget_user(self, view):
        with patch.object(view, "get_user") as mock:
            yield mock

    @fixture
    def mget_convention(self, view):
        with patch.object(view, "get_convention") as mock:
            yield mock

    def test_get_panel_time_when_not_present(
        self, view, mrequest, mget_active, mget_convention, mget_panel
    ):
        """
        ._get_panel_time should return empty panel time when it is not present.
        """
        mget_active.side_effect = NoResultFound()
        mrequest.matchdict["panel_uid"] = uuid4().hex
        mrequest.matchdict["convention_uid"] = uuid4().hex

        assert view._get_panel_time() == {
            "convention_uid": mrequest.matchdict["convention_uid"],
            "panel_uid": mrequest.matchdict["panel_uid"],
            "room_uid": None,
            "begin_date": mget_convention.return_value["begin_date"],
            "end_date": None,
            "panel": mget_panel.return_value,
        }
        mget_active.assert_called_once_with(
            mrequest.matchdict["convention_uid"], mrequest.matchdict["panel_uid"]
        )

    def test_get_panel_time_when_present(self, view, mrequest, mget_active):
        """
        ._get_panel_time should raise HTTPNotFound error when panel is not present.
        """
        mrequest.matchdict["panel_uid"] = uuid4().hex
        mrequest.matchdict["convention_uid"] = uuid4().hex
        assert view._get_panel_time() == mget_active.return_value
        mget_active.assert_called_once_with(
            mrequest.matchdict["convention_uid"], mrequest.matchdict["panel_uid"]
        )

    def test_validate(self, view, mget_panel_time, mget_user, mget_convention):
        """
        .validate should check if panel exists and if user is logged in
        """
        view.validate()
        mget_panel_time.assert_called_once_with()
        mget_user.assert_called_once_with()
        mget_convention.assert_called_once_with()

    def test_get(self, view, mget_panel_time):
        """
        .get should return serialized panel
        """
        uid = uuid4()
        mget_panel_time.return_value = {"uid": uid, "convention_uid": uid}

        assert view.get() == {"uid": uid.hex, "convention_uid": uid.hex}

    def test_patch(self, view, mrequest, mupdate_by_uid):
        """
        .patch should send to database proper update data
        """
        uid = uuid4().hex
        convention_uid = uuid4()
        panel_uid = uuid4()
        room_uid = uuid4()
        begin_date = datetime.now()
        end_date = datetime.now()
        mrequest.matchdict = {"panel_uid": uid}
        mrequest.json_body = {
            "convention_uid": convention_uid.hex,
            "panel_uid": panel_uid.hex,
            "room_uid": room_uid.hex,
            "begin_date": begin_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        view.patch()

        mupdate_by_uid.assert_called_once_with(
            uid,
            {
                "convention_uid": convention_uid,
                "panel_uid": panel_uid,
                "room_uid": room_uid,
                "begin_date": begin_date,
                "end_date": end_date,
            },
        )

    def test_delete(self, view, mrequest, mdelete):
        """
        .delete should delete object from the database
        """
        panel_uid = uuid4().hex
        convention_uid = uuid4().hex
        mrequest.matchdict = {"panel_uid": panel_uid, "convention_uid": convention_uid}

        view.delete()

        mdelete.assert_called_once_with(convention_uid, panel_uid)
