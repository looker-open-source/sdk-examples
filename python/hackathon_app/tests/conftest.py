import base64
import json
import os
import pathlib
import pytest  # type: ignore
from typing import Sequence, List, Dict

from google.oauth2 import service_account  # type: ignore
from googleapiclient import discovery  # type: ignore
from sheets import (
    Hackathon,
    Hackathons,
    Registration,
    Registrations,
    Sheets,
    User,
    Users,
    WhollySheet,
    converter,
    Projects,
)

import schema
from server import main


@pytest.fixture
def flask_client(
    spreadsheet,
):  # not using return value of fixture, but including it causes it to run
    with main.app.test_client() as client:
        yield client


@pytest.fixture(name="WhollySheet")
def instantiate_whollysheet(spreadsheet_client, spreadsheet):
    """Creates and returns an instance of WhollySheet"""

    client = spreadsheet_client.values()
    return WhollySheet(
        client=client,
        spreadsheet_id=spreadsheet["spreadsheetId"],
        sheet_name="users",
        structure=Sequence[User],
        key="email",
    )


@pytest.fixture(name="sheets")
def instantiate_sheets(spreadsheet, cred_file):
    """Creates and returns an instance of Sheets"""
    return Sheets(spreadsheet_id=spreadsheet["spreadsheetId"], cred_file=cred_file)


@pytest.fixture(name="users")
def instantiate_users(spreadsheet_client, spreadsheet):
    """Creates and returns an instance of Users"""
    client = spreadsheet_client.values()
    return Users(client=client, spreadsheet_id=spreadsheet["spreadsheetId"])


@pytest.fixture(name="hackathons")
def instantiate_hackathons(spreadsheet_client, spreadsheet):
    """Creates and returns an instance of Hackathons"""
    client = spreadsheet_client.values()
    return Hackathons(client=client, spreadsheet_id=spreadsheet["spreadsheetId"])


@pytest.fixture(name="registrations")
def instantiate_registrations(spreadsheet_client, spreadsheet):
    """Creates and returns an instance of Registrations"""
    client = spreadsheet_client.values()
    return Registrations(client=client, spreadsheet_id=spreadsheet["spreadsheetId"])


@pytest.fixture(name="projects")
def instantiate_projects(spreadsheet_client, spreadsheet):
    """Creates and returns an instance of Projects"""
    client = spreadsheet_client.values()
    return Projects(client=client, spreadsheet_id=spreadsheet["spreadsheetId"])


@pytest.fixture(scope="session")
def create_test_sheet(spreadsheet_client, test_data, drive_client):
    """Create a test sheet and populate it with test data"""
    request = spreadsheet_client.create(body=test_data)
    response = request.execute()
    yield response
    drive_client.files().delete(fileId=response["spreadsheetId"]).execute()


# TODO figure out why making this a fixture throws pytest errors
# @pytest.fixture(name="tsv_files", scope="session")
def get_tsv_files():
    path = "tests/data"
    files = [f"{path}/{f}" for f in os.listdir(path) if pathlib.Path(f).suffix == ".tsv"]
    return files


# TODO figure out why making this a fixture throws pytest errors
# @pytest.fixture(name="sheet_names", scope="session")
def get_sheet_names():
    files = [f for f in os.listdir("tests/data") if pathlib.Path(f).suffix == ".tsv"]
    # get the base name of the file without the path
    names = [os.path.splitext(pathlib.PurePath(f).name)[0] for f in files]
    return names


def sheet_pos(name: str) -> int:
    names = get_sheet_names()
    result = names.index(name)
    assert result >= 0
    return result

@pytest.fixture(name="spreadsheet")
def reset_test_sheet(create_test_sheet, test_data, spreadsheet_client, drive_client):
    """Reset spreadsheet values between tests."""

    # TODO why isn't this working as the variable for ranges in the body below?
    # tabs = get_sheet_names()
    # ranges = [f"{t}!A1:end" for t in tabs]   # ["users!A1:end", "hackathons!A1:end", "registrations!A1:end"]
    # print(ranges)
    spreadsheet_id = create_test_sheet["spreadsheetId"]
    spreadsheet_client.values().batchClear(
        spreadsheetId=spreadsheet_id,
        body={"ranges": ['projects!A1:end', 'registrations!A1:end', 'hackathons!A1:end', 'users!A1:end']},
    ).execute()

    # TODO make this a data-driven loop
    for sheet in create_test_sheet["sheets"]:
        if sheet["properties"]["title"] == "projects":
            project_sheet_id = sheet["properties"]["sheetId"]
        if sheet["properties"]["title"] == "registrations":
            registration_sheet_id = sheet["properties"]["sheetId"]
        if sheet["properties"]["title"] == "hackathons":
            hackathon_sheet_id = sheet["properties"]["sheetId"]
        if sheet["properties"]["title"] == "users":
            user_sheet_id = sheet["properties"]["sheetId"]

    updates = {
        "requests": [
            {
                "appendCells": {
                    "sheetId": project_sheet_id,
                    "fields": "userEnteredValue",
                    "rows": test_data["sheets"][sheet_pos("projects")]["data"][0]["rowData"],
                }
            },
            {
                "appendCells": {
                    "sheetId": registration_sheet_id,
                    "fields": "userEnteredValue",
                    "rows": test_data["sheets"][sheet_pos("registrations")]["data"][0]["rowData"],
                }
            },
            {
                "appendCells": {
                    "sheetId": hackathon_sheet_id,
                    "fields": "userEnteredValue",
                    "rows": test_data["sheets"][sheet_pos("hackathons")]["data"][0]["rowData"],
                }
            },
            {
                "appendCells": {
                    "sheetId": user_sheet_id,
                    "fields": "userEnteredValue",
                    "rows": test_data["sheets"][sheet_pos("users")]["data"][0]["rowData"],
                }
            },
        ]
    }
    spreadsheet_client.batchUpdate(spreadsheetId=spreadsheet_id, body=updates).execute()
    yield create_test_sheet


def find_sheet(test_data, name: str) -> List[Dict]:
    result = test_data["sheets"][sheet_pos(name)]
    assert result["properties"]["title"] == name
    return result


@pytest.fixture(name="test_projects")
def get_test_projects(test_data):
    """Returns a list of dicts representing the users sheet"""
    projects_sheet = find_sheet(test_data, "projects")
    return create_sheet_repr(projects_sheet, Projects)


@pytest.fixture(name="test_registrants")
def get_test_registrants(test_data):
    """Returns a list of dicts representing the registrations sheet"""
    registrations_sheet = find_sheet(test_data, "registrations")
    return create_sheet_repr(registrations_sheet, Registration)


@pytest.fixture(name="test_hackathons")
def get_test_hackathons(test_data):
    """Returns a list of dicts representing the hackathons sheet"""
    hackathons_sheet = find_sheet(test_data, "hackathons")
    return create_sheet_repr(hackathons_sheet, Hackathon)


@pytest.fixture(name="test_users")
def get_test_users(test_data):
    """Returns a list of dicts representing the users sheet"""
    users_sheet = find_sheet(test_data, "users")
    return create_sheet_repr(users_sheet, User)


def create_sheet_repr(sheet, model):
    """Converts a JSON representation of a sheet into a list of dicts. Each element
    in the list represents a row in the sheet, where each cell value can be accessed
    using the cell header as a key
    """
    header = get_header(sheet)
    data = get_data(sheet)
    result = converter.structure([dict(zip(header, d)) for d in data], Sequence[model])
    return result


def get_header(sheet):
    """Get the header as a list"""
    sheet_header = sheet["data"][0]["rowData"][0]["values"]
    header = ["id"]
    for cell in sheet_header:
        cell_value = cell["userEnteredValue"]["stringValue"]
        header.append(cell_value)
    return header


def get_data(sheet):
    """Return data (exc headers) from a sheet as a list of rows, with each
     row being a list representing all cell values in that row
     """
    rows_exc_header = sheet["data"][0]["rowData"][1:]
    data = []
    for id_, row in enumerate(rows_exc_header, start=2):
        row_data = [id_]
        for cell in row["values"]:
            cell_value = cell["userEnteredValue"]["stringValue"]
            row_data.append(cell_value)
        data.append(row_data)
    return data


@pytest.fixture(scope="session")
def test_data():
    """Load the test data"""
    # with open("tests/data/data.json", "r") as f:
    #     data = json.load(f)
    files = get_tsv_files()
    data = schema.import_sheet_data(files)
    return data


@pytest.fixture(scope="session")
def test_schema():
    """Load the hackathon schema"""
    with open("hackathon.schema", "r") as f:
        data = f.read()
    return data


@pytest.fixture(scope="session")
def spreadsheet_client(credentials):
    """Create a resource object to use the sheets API"""
    service = discovery.build("sheets", "v4", credentials=credentials)
    spreadsheet_client = service.spreadsheets()

    return spreadsheet_client


@pytest.fixture(scope="session")
def drive_client(credentials):
    """Create a resource object to use the drive API"""
    drive_client = discovery.build("drive", "v3", credentials=credentials)

    return drive_client


@pytest.fixture(scope="session")
def credentials(cred_file) -> service_account.Credentials:
    """Build a Credentials instance from file"""
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        cred_file, scopes=scopes
    )

    return credentials


@pytest.fixture(scope="session")
def cred_file():
    """Read the google json credentials file (base64 encoded) from the
    GOOGLE_APPLICATION_CREDENTIAL_ENCODED env variable, decode it and write
    it to google-creds.json
    """
    google_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIAL_ENCODED")
    assert google_creds
    file_name = "./google-creds.json"
    with open(file_name, "wb") as f:
        f.write(base64.b64decode(google_creds))

    yield file_name

    os.remove("./google-creds.json")
