from uuid import uuid4


class Model(object):
    def __init__(self, uid=None, created_at=None, updated_at=None):
        self.uid = uid or uuid4()
        self.created_at = created_at
        self.updated_at = updated_at
