import datetime
from typing import List

import sheets


def compare_hackathon(expected: sheets.Hackathon, actual: sheets.Hackathon):
    assert expected.id == actual.id
    assert expected.name == actual.name
    assert expected.date == actual.date
    assert expected.description == actual.description
    assert expected.duration_in_days == actual.duration_in_days
    assert expected.location == actual.location


def test_rows_returns_hackathons(
    hackathons: sheets.Hackathons, test_hackathons: List[sheets.Hackathon]
):
    """rows() should return a list of Hackathon objects"""
    all_hackathons = hackathons.rows()
    assert isinstance(all_hackathons, list)
    assert len(all_hackathons) == len(test_hackathons)

    hackathon = all_hackathons[0]
    expected = test_hackathons[0]
    compare_hackathon(expected, hackathon)


def test_get_upcoming_hackathons(
    hackathons: sheets.Hackathons, test_hackathons: List[sheets.Hackathon]
):
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    up_coming_expected = sorted(
        (h for h in test_hackathons if h.date >= now), key=lambda ht: ht.id
    )
    up_coming_actual = sorted(hackathons.get_upcoming(), key=lambda ht: ht.id)
    for index, actual in enumerate(up_coming_actual):
        compare_hackathon(up_coming_expected[index], actual)


def test_get_upcoming_hackathons_with_cutoff(
    hackathons: sheets.Hackathons, test_hackathons: List[sheets.Hackathon]
):
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    cutoff = now + datetime.timedelta(days=60)

    # setup some hackathons to occur within cutoff date
    # ensure we at most 3 hackathons so we don't decrement date into the past
    up_coming_expected = sorted(
        (h for h in test_hackathons if h.date >= now), key=lambda ht: ht.id
    )[:3]
    for d, hackathon in enumerate(up_coming_expected, start=1):
        hackathon.date = cutoff - datetime.timedelta(days=2 * d)
        hackathons.update(hackathon)
    assert len(up_coming_expected) > 0, "Bad fixture data setup"

    up_coming_actual = sorted(
        hackathons.get_upcoming(cutoff=cutoff), key=lambda ht: ht.id
    )
    assert len(up_coming_actual) > 0
    for hackathon in up_coming_actual:
        assert hackathon.date < cutoff
