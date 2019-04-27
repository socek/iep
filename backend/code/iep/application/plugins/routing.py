from sapp.plugins.pyramid.routing import Routing
from iep.auth.routing import auth_routing


class IAPRouting(Routing):
    def make(self):
        auth_routing(self)
