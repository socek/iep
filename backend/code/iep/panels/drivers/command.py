from iep.application.drivers import Command

from .dbmodels import PanelData
from .query import PanelsQuery


class PanelsCommand(Command):
    model = PanelData
    _query = PanelsQuery
