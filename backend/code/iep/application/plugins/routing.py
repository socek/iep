from sapp.plugins.pyramid.routing import Routing

from iep.auth.routing import auth_routing
from iep.conventions.routing import conventions_routing
from iep.grid.routing import panel_times_routing
from iep.panels.routing import panels_routing
from iep.rooms.routing import rooms_routing


class IAPRouting(Routing):
    def make(self):
        auth_routing(self)
        panels_routing(self)
        rooms_routing(self)
        conventions_routing(self)
        panel_times_routing(self)
