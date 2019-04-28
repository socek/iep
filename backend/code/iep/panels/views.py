from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest

from iep import app
from iep.panels.drivers.query import PanelsQuery
from iep.panels.schemas import PanelSchema
from iep.application.views import RestfulView

# Gather
# Get
# Manipulate
# Store
# Result


class PanelsView(RestfulView):
    def _get_panels(self):
        with app("dbsession") as db:
            query = PanelsQuery(db)
            return query.list_active()

    def get(self):
        """
        List all active panels.
        """
        panels = self._get_panels()
        schema = PanelSchema(many=True)
        result = schema.dump(panels)
        return result
