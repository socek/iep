from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime

from iep.application.drivers.dbmodel import Base


class TestBase(object):
    def test_update_model_after_commit(self):
        """
        ._update_model_after_commit should update values in provided model
        """
        model = MagicMock()
        base = Base()

        base.uid = uuid4()
        base.is_active = True
        base.created_at = datetime.now()
        base.updated_at = datetime.now()

        base._update_model_after_commit(model)

        assert model.uid == base.uid
        assert model.created_at == base.created_at
        assert model.updated_at == base.updated_at

        assert model.is_active != base.is_active
