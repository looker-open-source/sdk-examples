import base64
from google.oauth2 import service_account
from googleapiclient import discovery

import sheets
import schema
import os
from tests import conftest


def credential_file():
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
    os.remove(file_name)


def credentials(cred_file) -> service_account.Credentials:
    """Build a Credentials instance from file"""
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    return service_account.Credentials.from_service_account_file(
        cred_file, scopes=scopes
    )


def spreadsheet_client(sheet_creds):
    """Create a resource object to use the sheets API"""
    service = discovery.build("sheets", "v4", credentials=sheet_creds)
    return service.spreadsheets()


def compare_schema(test: str, expected: schema.SchemaSheet, actual: schema.SchemaSheet):
    delta = expected.compare(actual)
    diff = "\n".join(
        [d.debug() for d in delta if d.diff != schema.Difference.OldName and d.diff != schema.Difference.Columns]
    )
    if len(diff) > 0:
        status = "MISMATCH: "
    else:
        status = "SAME: "
    print(f"\n{status}{test}")
    if len(diff) > 0:
        print(diff)


if __name__ == "__main__":
    print("Checking various schemas. Please wait ...")
    master = schema.SchemaSheet(filename="hackathon.schema")
    model = sheets.get_model_schema()
    files_to_import = conftest.get_tsv_files()
    imported = schema.SchemaSheet(lines="\n".join(schema.import_schema(files_to_import)))
    compare_schema("hackathon.schema vs. code", master, model)
    compare_schema("hackathon.schema vs. imported files", master, imported)
    compare_schema("code vs. imported files", model, imported)

    # check the schema on any sheets that may have ids specified
    sheets_to_check = os.getenv("SHEETS_TO_CHECK", "")
    # sheets_to_check = "1PajtcfMeEogN24MjTYtQFTc3_elCMvS9TeVCI0bhYek,1D-HIkl3LdYGVlMu7F5XAnoUM-JkKtDQgmkkVOrEL3ds"
    sheet_ids = sheets_to_check.split(",")
    if not sheets_to_check:
        print("\nTo check live Google sheets, export SHEETS_TO_CHECK=sheetId1,sheetId2,...")
    else:
        print(f"\nChecking {len(sheet_ids)} live sheets {sheets_to_check} ...")
        creds = credentials(credential_file())
        for sid in sheet_ids:
            live = spreadsheet_client()


