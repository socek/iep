from json.decoder import JSONDecodeError

from marshmallow.exceptions import ValidationError
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotAcceptable

from sapp.plugins.pyramid.views import RestfulView as BaseRestfulView


class RestfulView(BaseRestfulView):
    def get_validated_fields(self, schema, **kwargs):
        try:
            return schema.load(self.request.json_body, **kwargs)
        except JSONDecodeError:
            raise HTTPNotAcceptable()
        except ValidationError as error:
            print(error)
            raise HTTPBadRequest(json=error.messages)

    def validate(self):
        pass

    def __call__(self):
        self.validate()
        method = self.methods[self.request.method]
        return method()
