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
        accepted=None,
        convention_uid=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.name = name
        self.description = description
        self.additional = additional
        self.creator = creator
        self.room = room
        self.accepted = accepted
        self.convention_uid = convention_uid

    def to_dict(self):
        return dict(
            uid=self.uid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            description=self.description,
            additional=self.additional,
            creator=self.creator,
            room=self.room,
            accepted=self.accepted,
            convention_uid=self.convention_uid,
        )
