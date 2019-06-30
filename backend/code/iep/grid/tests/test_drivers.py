from datetime import datetime

from pytest import fixture
from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import IntegrationFixture
from iep.grid.drivers.command import delete
from iep.grid.drivers.command import save_new
from iep.grid.drivers.command import upsert
from iep.grid.drivers.query import get_active
from iep.grid.drivers.query import get_active_by_uid
from iep.grid.drivers.query import is_time_frame_avalible
from iep.grid.drivers.query import list_active_by_convention
from iep.panels.drivers import command as panel_command


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

    def test_get_active_when_missing(self):
        """
        get_active should raise NoResultFound when item is not found.
        """
        with raises(NoResultFound):
            get_active("x", "x")


class TestIsTimeFrameAvalible(IntegrationFixture):
    @fixture
    def panel_time(self, convention1_uid, panel1_uid, room1_uid):
        begin_date = datetime(year=2019, month=6, day=3, hour=17)
        end_date = datetime(year=2019, month=6, day=3, hour=19)
        upsert(convention1_uid, panel1_uid, room1_uid, begin_date, end_date)
        yield (begin_date, end_date)
        delete(convention1_uid, panel1_uid)

    @fixture
    def panel3_uid(self, convention1_uid):
        uid = panel_command.save_new(
            name="panel 3", convention_uid=convention1_uid, minutes=60
        )
        yield uid
        panel_command.force_delete(uid)

    def test_when_time_is_avalible(self, convention1_uid, room1_uid, panel3_uid):
        """
        IsTimeFrameAvalible should return True if no other timefrime is
        overlapsing new time frame
        """
        assert (
            is_time_frame_avalible(
                convention1_uid,
                room1_uid,
                datetime(year=2019, month=6, day=3, hour=19),
                datetime(year=2019, month=6, day=3, hour=20),
            )
            is True
        )

    def test_when_starting_at_the_end_of_anthoer(
        self, convention1_uid, room1_uid, panel_time, panel3_uid
    ):
        """
        IsTimeFrameAvalible should return True if another timeframe is ending
        when new time frame starts
        """
        assert (
            is_time_frame_avalible(
                convention1_uid,
                room1_uid,
                datetime(year=2019, month=6, day=3, hour=19),
                datetime(year=2019, month=6, day=3, hour=20),
            )
            is True
        )

    def test_when_ending_at_the_start_of_anthoer(
        self, convention1_uid, room1_uid, panel_time, panel3_uid
    ):
        """
        IsTimeFrameAvalible should return True if another timeframe is starting
        when new time frame ends
        """
        assert (
            is_time_frame_avalible(
                convention1_uid,
                room1_uid,
                datetime(year=2019, month=6, day=3, hour=16),
                datetime(year=2019, month=6, day=3, hour=17),
            )
            is True
        )

    def test_when_another_panel_is_starting(
        self, convention1_uid, room1_uid, panel_time, panel3_uid
    ):
        """
        IsTimeFrameAvalible should return False if another timeframe is starting
        during new time frame
        """
        assert (
            is_time_frame_avalible(
                convention1_uid,
                room1_uid,
                datetime(year=2019, month=6, day=3, hour=16, minute=30),
                datetime(year=2019, month=6, day=3, hour=17, minute=30),
            )
            is False
        )

    def test_when_another_panel_is_ending(
        self, convention1_uid, room1_uid, panel_time, panel3_uid
    ):
        """
        IsTimeFrameAvalible should return False if another timeframe is ending
        during new time frame
        """
        assert (
            is_time_frame_avalible(
                convention1_uid,
                room1_uid,
                datetime(year=2019, month=6, day=3, hour=18, minute=30),
                datetime(year=2019, month=6, day=3, hour=19, minute=30),
            )
            is False
        )

    def test_when_another_panel_is_beyond(
        self, convention1_uid, room1_uid, panel_time, panel3_uid
    ):
        """
        IsTimeFrameAvalible should return False if another timeframe is starting
        before and ending after new time frame
        """
        assert (
            is_time_frame_avalible(
                convention1_uid,
                room1_uid,
                datetime(year=2019, month=6, day=3, hour=17, minute=30),
                datetime(year=2019, month=6, day=3, hour=18, minute=30),
            )
            is False
        )

    def test_when_checking_the_same_panel(
        self, convention1_uid, room1_uid, panel_time, panel1_uid,
    ):
        """
        IsTimeFrameAvalible should ignore provided panel, so it will not false
        unvalidate the same panel
        """
        assert (
            is_time_frame_avalible(
                convention1_uid,
                room1_uid,
                panel_time[0],
                panel_time[1],
                panel1_uid
            )
            is True
        )
