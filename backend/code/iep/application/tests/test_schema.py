from unittest.mock import MagicMock
from uuid import uuid4

from pytest import fixture

from iep.application.schemas import ModelSchema


class ExampleSchema(ModelSchema):
    def __init__(self):
        super().__init__()
        self.MODEL = MagicMock()


class TestModelSchema(object):
    @fixture
    def schema(self):
        return ExampleSchema()

    def test_make_dict(self, schema):
        """
        .make_dict should return data in dict format.
        """
        uid = uuid4()
        obj = MagicMock()
        obj.to_dict.return_value = {"uid": uid}
        assert schema.dump(obj) == {"uid": uid.hex}
        obj.to_dict.assert_called_once_with()

    def test_make_model(self, schema):
        """
        .make_model should create model from serialized data
        """
        assert schema.make_model({"test": 1}) == schema.MODEL.return_value
        schema.MODEL.assert_called_once_with(test=1)
