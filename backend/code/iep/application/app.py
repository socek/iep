from sapp.plugins.logging import LoggingPlugin
from sapp.plugins.pyramid.configurator import ConfiguratorWithPyramid
from sapp.plugins.pyramid.plugins import RoutingPlugin
from sapp.plugins.settings import SettingsPlugin
from sapp.plugins.sqlalchemy.plugin import DatabasePlugin

from iep.application.plugins.routing import IAPRouting


class IAPConfigurator(ConfiguratorWithPyramid):
    def append_plugins(self):
        self.add_plugin(SettingsPlugin("iep.application.settings"))
        self.add_plugin(LoggingPlugin())
        self.add_plugin(DatabasePlugin("dbsession"))
        self.add_plugin(RoutingPlugin(IAPRouting))
