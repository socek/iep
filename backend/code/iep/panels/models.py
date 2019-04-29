from iep.application.model import Model


class Panel(Model):
    def __init__(
        self,
        uid=None,
        created_at=None,
        updated_at=None,
        name=None,
        description=None,
        additional=None,
        creator=None,
        room=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.name = name
        self.description = description
        self.additional = additional
        self.creator = creator
        self.room = room

