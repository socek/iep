from bcrypt import checkpw
from bcrypt import gensalt
from bcrypt import hashpw

from iep.application.model import Model


class User(Model):
    def __init__(
        self,
        uid,
        created_at=None,
        updated_at=None,
        name=None,
        email=None,
        is_admin=None,
        password=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.name = name
        self.email = email
        self.is_admin = is_admin
        self.password = password

    def do_password_match(self, password):
        """
        Validate if provided password match with the password from the model.
        """
        if self.password:
            return checkpw(password.encode("utf8"), self.password)
        else:
            return False

    def set_password(self, password):
        self.password = hashpw(password.encode("utf8"), gensalt())

    def to_dict(self):
        return {
            'uid': self.uid,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin,
            'password': self.password,
        }
