import base64
import json
import os
import pathlib
import pytest  # type: ignore
from typing import Sequence, List, Dict

from google.oauth2 import service_account  # type: ignore
from googleapiclient import discovery  # type: ignore


def get_tsv_files():
    path = "tests/data"
    files = [f"{path}/{f}" for f in os.listdir(path) if pathlib.Path(f).suffix == ".tsv"]
    return files


def get_sheet_names():
    files = [f for f in os.listdir("tests/data") if pathlib.Path(f).suffix == ".tsv"]
    # get the base name of the file without the path
    names = [os.path.splitext(pathlib.PurePath(f).name)[0] for f in files]
    return names

#
# def sheet_pos(name: str) -> int:
#     names = get_sheet_names()
#     result = names.index(name)
#     assert result >= 0
#     return result
#
#
# def find_sheet(test_data, name: str) -> List[Dict]:
#     result = test_data["sheets"][sheet_pos(name)]
#     assert result["properties"]["title"] == name
#     return result
#
#
# def get_test_projects(test_data):
#     """Returns a list of dicts representing the users sheet"""
#     projects_sheet = find_sheet(test_data, "projects")
#     return create_sheet_repr(projects_sheet, Projects)
#
#
# def get_test_registrants(test_data):
#     """Returns a list of dicts representing the registrations sheet"""
#     registrations_sheet = find_sheet(test_data, "registrations")
#     return create_sheet_repr(registrations_sheet, Registration)
#
#
# def get_test_hackathons(test_data):
#     """Returns a list of dicts representing the hackathons sheet"""
#     hackathons_sheet = find_sheet(test_data, "hackathons")
#     return create_sheet_repr(hackathons_sheet, Hackathon)
#
#
# def get_test_users(test_data):
#     """Returns a list of dicts representing the users sheet"""
#     users_sheet = find_sheet(test_data, "users")
#     return create_sheet_repr(users_sheet, User)
#
#
# def create_sheet_repr(sheet, model):
#     """Converts a JSON representation of a sheet into a list of dicts. Each element
#     in the list represents a row in the sheet, where each cell value can be accessed
#     using the cell header as a key
#     """
#     header = get_header(sheet)
#     data = get_data(sheet)
#     result = converter.structure([dict(zip(header, d)) for d in data], Sequence[model])
#     return result
#
#
# def get_header(sheet):
#     """Get the header as a list"""
#     sheet_header = sheet["data"][0]["rowData"][0]["values"]
#     header = ["row_id"]
#     for cell in sheet_header:
#         cell_value = cell["userEnteredValue"]["stringValue"]
#         header.append(cell_value)
#     return header
#
#
# def get_data(sheet):
#     """
#     Return data (exc headers) from a sheet as a list of rows, with each
#     row being a list representing all cell values in that row
#     """
#     rows_exc_header = sheet["data"][0]["rowData"][1:]
#     data = []
#     for id_, row in enumerate(rows_exc_header, start=2):
#         row_data = [id_]
#         for cell in row["values"]:
#             cell_value = cell["userEnteredValue"]["stringValue"]
#             row_data.append(cell_value)
#         data.append(row_data)
#     return data


def spreadsheet_client(creds):
    """Create a resource object to use the sheets API"""
    service = discovery.build("sheets", "v4", credentials=creds)
    return service.spreadsheets()


def drive_client(creds):
    """Create a resource object to use the drive API"""
    return discovery.build("drive", "v3", credentials=creds)


def credentials(file_name) -> service_account.Credentials:
    """Build a Credentials instance from file"""
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    return service_account.Credentials.from_service_account_file(
        file_name, scopes=scopes
    )


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

    # TODO should this be a yield?
    return file_name

    # os.remove("./google-creds.json")
