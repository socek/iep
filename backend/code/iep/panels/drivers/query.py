from iep.application.drivers import Query

from .dbmodels import PanelData


class PanelsQuery(Query):
    model = PanelData
