from pytest import raises

from iep.application.drivers.query import NoResultFound
from iep.application.testing import IntegrationFixture
from iep.auth.drivers import command as user_command
from iep.auth.drivers import query as user_query


class TestUserDriver(IntegrationFixture):
    def test_find_by_email(self, user):
        assert user_query.find_by_email(self.user_data["email"]).uid == user.uid

    def test_find_by_email_with_no_user(self):
        assert user_query.find_by_email(self.user_data["email"] + 'c') is None

    def test_create(self, user):
        assert user.uid
        assert user.created_at
        assert user.updated_at
        assert user.name == self.user_data["name"]
        assert user.email == self.user_data["email"]
        assert user.is_admin == self.user_data["is_admin"]
        assert user.password != self.user_data["password"]
        assert type(user.password) == bytes

    def test_get_active_by_uid(self, user):
        model = user_query.get_active_by_uid(user.uid)
        assert model.uid == user.uid
        assert model.created_at == user.created_at
        assert model.updated_at == user.updated_at
        assert model.name == user.name
        assert model.email == user.email
        assert model.is_admin == user.is_admin
        assert model.password == user.password

    def test_get_active_by_uid_with_bad_uid(self):
        """
        .get_active_by_uid should raise NoResultFound when uuid is malformed
        """
        with raises(NoResultFound):
            user_query.get_active_by_uid("x")

    def test_delete(self, dynamic_user):
        user_command.delete_by_uid(dynamic_user.uid)

        with raises(NoResultFound):
            user_query.get_active_by_uid(dynamic_user.uid)

        result = [user["uid"] for user in user_query.list_active()]
        assert dynamic_user.uid not in result

    def test_list_active(self, user):
        data = list(user_query.list_active())
        assert len(data) == 1
        assert data[0]["uid"] == user.uid
        assert data[0]["created_at"] == user.created_at
        assert data[0]["updated_at"] == user.updated_at
        assert data[0]["name"] == user.name
        assert data[0]["email"] == user.email
        assert data[0]["is_admin"] == user.is_admin
        assert data[0]["password"] == user.password

    def test_save_with_wrong_argument(self):
        """
        save_new should raise error when trying to save not existing parameter
        """
        with raises(AttributeError):
            user_command.save_new(something=True)
