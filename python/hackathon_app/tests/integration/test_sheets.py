import datetime
from typing import cast, Sequence

from sheets import User, Users, DATE_FORMAT, Registrant, Registrations, Sheets


def test_gets_all_hackathons(sheets: Sheets, test_data):
    """get_hackathons() should return all active hackathons."""
    hackathons = sheets.get_hackathons()
    assert isinstance(hackathons, list)
    assert len(hackathons) > 0


def test_register_user_registers(
    sheets: Sheets, users: Users, registrations: Registrations, test_data
):
    """register_user() should register new users by adding them to the Users sheet
    and to the Registrations sheet
    """
    new_user = User(
        first_name="New",
        last_name="Registrant",
        email="newregistrant@newompany.com",
        organization="New Company",
        tshirt_size="M",
    )
    sheets.register_user(hackathon="sanfrancisco_2019", user=new_user)

    all_users = users.rows()
    last_inserted_user = all_users[-1]
    assert last_inserted_user.first_name == new_user.first_name
    assert last_inserted_user.last_name == new_user.last_name
    assert last_inserted_user.email == new_user.email
    assert last_inserted_user.date_created == datetime.datetime.strptime(
        datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT
    )
    assert last_inserted_user.organization == new_user.organization
    assert last_inserted_user.tshirt_size == new_user.tshirt_size

    all_registrants = registrations.rows()
    last_registrant = all_registrants[-1]
    assert last_registrant.user_email == new_user.email
    assert last_registrant.hackathon_name == "sanfrancisco_2019"
    assert last_registrant.date_registered == datetime.datetime.strptime(
        datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT
    )
    assert last_registrant.attended is None


def test_register_user_registers_when_user_exists(
    test_users, sheets: Sheets, users: Users, registrations: Registrations
):
    """register_user() should register a user by adding them to the Registrations sheet
    if user already exists in the Users sheet but not in the Registrations sheet.
    """
    existing_user = cast(User, test_users[0])
    new_user = User(
        first_name=existing_user.first_name,
        last_name=existing_user.last_name,
        email=existing_user.email,
        organization=existing_user.organization,
        tshirt_size=existing_user.tshirt_size,
    )
    sheets.register_user(hackathon="newhackathon_2019", user=new_user)

    all_users = users.rows()
    assert len(all_users) == len(test_users)

    all_registrants = registrations.rows()
    last_registrant = all_registrants[-1]
    assert last_registrant.user_email == existing_user.email
    assert last_registrant.hackathon_name == "newhackathon_2019"
    assert last_registrant.date_registered == datetime.datetime.strptime(
        datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT
    )
    assert last_registrant.attended is None


def test_register_updates_user_if_user_is_registered(
    users: Users,
    test_users: Sequence[User],
    test_registrants: Sequence[Registrant],
    sheets: Sheets,
    registrations: Registrations,
):
    """register_user() should update the user but not re-register if user is already registered"""
    existing_registrant = cast(Registrant, test_registrants[0])
    for user in test_users:
        if user.email == existing_registrant.user_email:
            updated_user = user
            break
    assert isinstance(updated_user, User)

    updated_user.first_name = "updated_first"
    updated_user.last_name = "updated_last"
    updated_user.organization = "updated_org"
    updated_user.tshirt_size = "update_size"

    sheets.register_user(
        hackathon=existing_registrant.hackathon_name, user=updated_user
    )

    retrieved_user = users.find("email", existing_registrant.user_email)
    assert isinstance(retrieved_user, User)
    assert retrieved_user.first_name == updated_user.first_name
    assert retrieved_user.last_name == updated_user.last_name
    assert retrieved_user.organization == updated_user.organization
    assert retrieved_user.tshirt_size == updated_user.tshirt_size
