import datetime

from sheets import Registration, Registrations


def compare_reg(expected: Registration, actual: Registration):
    assert expected.id == actual.id
    assert expected.user_id == actual.user_id
    assert expected.hackathon_id == actual.hackathon_id
    assert expected.date_registered == actual.date_registered
    assert expected.attended == actual.attended


def test_rows_returns_registrants(registrations: Registrations, test_registrants):
    """rows() should return a list of Registration objects"""
    all_registrations = registrations.rows()
    assert isinstance(all_registrations, list)
    assert len(all_registrations) == len(test_registrants)

    registrant = all_registrations[0]
    expected = test_registrants[0]
    compare_reg(expected, registrant)


def test_is_registered_returns_true_for_existing_registrants(
    registrations: Registrations, test_registrants
):
    """is_registered(registrant) should return True for already registered users"""
    registrant = test_registrants[0]
    existing_registrant = Registration(
        user_id=registrant.user_id,
        hackathon_id=registrant.hackathon_id,
        date_registered=registrant.date_registered,
        attended=bool(registrant.attended),
    )
    assert registrations.is_registered(existing_registrant)


def test_is_registered_returns_false_for_new_registrants(
    registrations: Registrations, test_registrants
):
    """is_registered(registrant) should return False for already registered users"""
    new_registrant = Registration(
        user_id="newid",
        hackathon_id="brand_new_hackathon",
        date_registered=datetime.date.today(),
        attended=None,
    )
    assert not registrations.is_registered(new_registrant)


def test_register(registrations: Registrations):
    """register() should append new registrants to registrations sheets"""
    new_registrant = Registration(
        user_id="newid",
        hackathon_id="brand_new_hackathon",
        date_registered=datetime.datetime.now(),
        attended=None,
    )
    assert not registrations.is_registered(new_registrant)
    registrations.register(new_registrant)
    assert registrations.is_registered(new_registrant)
