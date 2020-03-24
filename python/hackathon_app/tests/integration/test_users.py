import datetime

from sheets import User, Users


def compare_user(expected: User, actual: User):
    assert expected.id == actual.id
    assert expected.email == actual.email
    assert expected.first_name == actual.first_name
    assert expected.last_name == actual.last_name
    assert expected.client_id == actual.client_id
    assert expected.client_secret == actual.client_secret
    assert expected.date_created == actual.date_created
    assert expected.organization == actual.organization
    assert expected.org_role == actual.org_role
    assert expected.setup_link == actual.setup_link


def test_rows_returns_users(users: Users, test_users):
    """rows() should return a list of User objects"""
    all_users = users.rows()
    assert isinstance(all_users, list)
    assert len(all_users) == len(test_users)

    user = all_users[0]
    expected = test_users[0]
    compare_user(expected, user)


def test_find_returns_existing_user(users: Users, test_users):
    """find(user) returns True if user already exists"""
    expected = test_users[0]
    actual = users.find(expected.id)
    compare_user(expected, actual)


def test_find_returns_false_non_existent_user(users: Users):
    """find(user) returns False for new users"""
    assert not users.find("no-one-has-this-id")


def test_create_user(users: Users):
    """create(user) should add a user to the users sheet"""
    new_user = User(
        id="hi",
        first_name="Hundy",
        last_name="P",
        email="hundyp@company.com",
        organization="company",
        org_role="BI analyst",
        tshirt_size="M",
    )
    users.save(new_user)
    all_users = users.rows()
    user = all_users[-1]
    compare_user(user, new_user)
    assert user.date_created < datetime.datetime.now(tz=datetime.timezone.utc)


def test_update_user_updates(users: Users):
    """update(user) should modify existing users in the users sheet. The user's
    id is used to uniquely identify a user and cannot be amended from the front end.
    """
    all_users = users.rows()
    updated_user = all_users[0]
    updated_user.first_name = "updated_first"
    updated_user.last_name = "updated_last"
    updated_user.organization = "updated_org"
    updated_user.organization = "updated_role"
    updated_user.tshirt_size = "update_size"
    users.save(updated_user)

    user = users.find(updated_user.id)
    assert isinstance(user, User)
    compare_user(user, updated_user)
