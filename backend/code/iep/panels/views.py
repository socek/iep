from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest

from iep import app
from iep.application.views import RestfulView
from iep.panels.drivers.query import list_active
from iep.panels.schemas import PanelSchema
from iep.panels.drivers.command import save_new




class PanelsView(RestfulView):
    def get(self):
        """
        List all active panels.
        """
        return list_active()

    def put(self):
        """
        Create new bill for logged in user.
        """
        schema = PanelSchema()
        panel = self.get_validated_fields(schema, partial=("uid",))
        uid = save_new(panel)
        return {
            'is_success': True,
            'uid': uid
        }
