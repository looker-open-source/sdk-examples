from datetime import datetime

from google.oauth2 import service_account  # type: ignore
from googleapiclient import discovery  # type: ignore

from typing import Sequence, List, Dict


class Sheets:
    """An API for manipulating the Google Sheet containing hackathon data."""

    def __init__(self, spreadsheet_id):
        scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets",
        ]

        credentials = service_account.Credentials.from_service_account_file(
            "jaxdata-a93316beb3a0.json", scopes=scopes
        )

        service = discovery.build("sheets", "v4", credentials=credentials)
        self.spreadsheet = service.spreadsheets().values()
        self.id = spreadsheet_id

    def get_hackathons(self):
        """Get names of active hackathons."""
        hackathons_table = self.spreadsheet.get(
            spreadsheetId=self.id, range="hackathons!A1:end"
        ).execute()
        data = hackathons_table["values"][1:]
        date_index = hackathons_table["values"][0].index("date")
        hackathons = []
        for row in data:
            if datetime.strptime(row[date_index], "%m/%d/%Y") >= datetime.now():
                hackathons.append(row[1])
        return hackathons

    def register_user(
        self,
        hackathon: str,
        first_name: str,
        last_name: str,
        email: str,
        company: str,
        country: str,
        tshirt_size: str,
    ):
        """Register user to a hackathon"""
        if not self._is_created(email):
            self.create_user(
                first_name, last_name, email, company, country, tshirt_size
            )
        self._register_user(email, hackathon)
        return

    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        company: str,
        country: str,
        tshirt_size: str,
    ):
        """Append user details to users sheet."""
        data = {
            "values": [
                [
                    first_name,
                    last_name,
                    email,
                    company,
                    country,
                    datetime.now().strftime("%m/%d/%Y"),
                    tshirt_size,
                ]
            ]
        }
        request = self.spreadsheet.append(
            spreadsheetId=self.id,
            range="users!A1:END",
            insertDataOption="INSERT_ROWS",
            valueInputOption="RAW",
            body=data,
        )
        request.execute()
        return

    def _is_created(self, email: str) -> bool:
        """Check if user already exists in the users sheet."""
        users = self.get_users()
        found = False
        for u in users:
            if u["email"] == email:
                found = True
                break
        return found

    def get_users(self):
        """Get users from the users sheets."""
        resp = self.spreadsheet.get(
            spreadsheetId=self.id, range="users!A1:end"
        ).execute()
        users = self._convert_to_dict(resp["values"])
        return users

    def _convert_to_dict(self, data) -> Sequence[Dict[str, str]]:
        # TODO: convert columns to proper type before returning
        # TODO: abstract this into a cattr structure
        result: List[Dict[str, str]] = [dict(zip(data[0], r)) for r in data[1:]]
        return result
