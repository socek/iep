from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

from pytest import fixture

from iep.application.drivers.dbmodel import Base


class TestBase(object):
    @fixture
    def base(self):
        return Base()

    @fixture
    def mto_dict(self, base):
        with patch.object(base, "to_dict") as mock:
            yield mock

    def test_update_model_after_commit(self, base):
        """
        ._update_model_after_commit should update values in provided model
        """
        model = MagicMock()

        base.uid = uuid4()
        base.is_active = True
        base.created_at = datetime.now()
        base.updated_at = datetime.now()

        base._update_model_after_commit(model)

        assert model.uid == base.uid
        assert model.created_at == base.created_at
        assert model.updated_at == base.updated_at

        assert model.is_active != base.is_active

    def test_to_model_when_using_model(self, base, mto_dict):
        """
        When using model, to_model() should return the model.
        """
        cls = MagicMock()
        base._model = cls

        base.uid = uuid4()
        base.is_active = True
        base.created_at = datetime.now()
        base.updated_at = datetime.now()

        assert base.to_model() == cls.return_value
        cls.assert_called_once_with(**mto_dict.return_value)

    def test_to_model_when_not_using_model(self, base, mto_dict):
        """
        When ._model is not specyfied, to_model() should return dict.
        """
        base.uid = uuid4()
        base.is_active = True
        base.created_at = datetime.now()
        base.updated_at = datetime.now()

        assert base.to_model() == mto_dict.return_value
