from iep.application.drivers import Command

from .dbmodels import UserData
from .query import UserQuery


class UserCommand(Command):
    model = UserData
    _query = UserQuery
