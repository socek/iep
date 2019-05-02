from sapp.plugins.pyramid.routing import Routing

from iep.auth.routing import auth_routing
from iep.panels.routing import panels_routing


class IAPRouting(Routing):
    def make(self):
        auth_routing(self)
        panels_routing(self)
