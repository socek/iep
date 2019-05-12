from marshmallow.fields import DateTime
from marshmallow.fields import String

from iep.application.schemas import DataModelSchema


class ConventionSchema(DataModelSchema):
    name = String()
    start_date = DateTime()
    end_date = DateTime()
