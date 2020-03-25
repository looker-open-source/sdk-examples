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
