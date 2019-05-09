from marshmallow import Schema as BaseSchema
from marshmallow import post_load
from marshmallow import pre_dump
from marshmallow.fields import String
from marshmallow.fields import UUID as BaseUUID
from marshmallow.validate import Length

not_blank = Length(min=1, error="Field can not be blank")


class UUID(BaseUUID):
    def _serialize(self, value, attr, obj):
        validated = self._validated(value).hex if value is not None else None
        return super(String, self)._serialize(validated, attr, obj)


class ModelSchema(BaseSchema):
    MODEL = None
    uid = UUID(required=True, allow_none=False)

    @pre_dump
    def make_dict(self, obj):
        """
        Serialize to dict object.
        """
        return obj if isinstance(obj, dict) else obj.to_dict()

    @post_load
    def make_model(self, data):
        """
        Create model from serialized data.
        """
        return self.MODEL(**data)


class DataModelSchema(BaseSchema):
    uid = UUID(required=True, allow_none=False)

    @pre_dump
    def make_dict(self, obj):
        """
        Serialize to dict object.
        """
        return obj if isinstance(obj, dict) else obj.to_dict()
