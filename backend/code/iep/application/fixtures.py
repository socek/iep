from datetime import datetime

from pytest import fixture

from iep.conventions.drivers import command as convention_command
from iep.grid.drivers import command as paneltime_command
from iep.panels.drivers import command as panel_command
from iep.rooms.drivers import command as room_command


class FixturesMixin(object):
    # Fixtures:
    # convention1
    # |- panel1
    # |- room1
    # |- room2
    # |- paneltime1
    #
    # convention2
    #

    @fixture
    def convention1_uid(self):
        uid = convention_command.save_new(
            name="convention 1",
            start_date=datetime(year=2019, month=6, day=3, hour=16),
            end_date=datetime(year=2019, month=6, day=5, hour=16),
        )
        yield uid
        convention_command.force_delete(uid)

    @fixture
    def panel1_uid(self, convention1_uid):
        uid = panel_command.save_new(name="panel 1", convention_uid=convention1_uid, minutes=120)
        yield uid
        panel_command.force_delete(uid)

    @fixture
    def room1_uid(self, convention1_uid):
        uid = room_command.save_new(name="room 1", convention_uid=convention1_uid)
        yield uid
        room_command.force_delete(uid)

    @fixture
    def room2_uid(self, convention1_uid):
        uid = room_command.save_new(name="room 2", convention_uid=convention1_uid)
        yield uid
        room_command.force_delete(uid)

    @fixture
    def paneltime1_uid(self, convention1_uid, panel1_uid, room1_uid):
        uid = paneltime_command.save_new(
            convention_uid=convention1_uid, panel_uid=panel1_uid, room_uid=room1_uid
        )
        yield uid
        paneltime_command.force_delete(uid)

    @fixture
    def convention2_uid(self):
        uid = convention_command.save_new(name="convention 2")
        yield uid
        convention_command.force_delete(uid)
