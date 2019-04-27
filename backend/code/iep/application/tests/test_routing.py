from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture

from iep.application.plugins.routing import IAPRouting


class TestIAPRouting(object):
    @fixture
    def madd(self):
        with patch.object(IAPRouting, "add") as mock:
            yield mock

    @fixture
    def mwsgi(self):
        return MagicMock()

    def test_routing(self, madd, mwsgi):
        """
        This is syntax check of the routing.
        """
        IAPRouting(mwsgi).make()

        madd.assert_not_called()
