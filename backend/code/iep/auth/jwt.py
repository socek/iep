from jwt import decode
from jwt import encode
from sapp import Decorator

from iep import app


@Decorator(app, "settings")
def encode_jwt_from_user(user, settings):
    payload = {"uid": user.uid}
    return encode(
        payload, settings["jwt:secret"], algorithm=settings["jwt:algorithm"]
    ).decode("utf8")


@Decorator(app, "settings")
def decode_jwt(token, settings):
    return decode(token, settings["jwt:secret"], algorithms=[settings["jwt:algorithm"]])
