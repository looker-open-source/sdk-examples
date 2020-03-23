from pprint import pprint
from typing import Dict, Generic, List, Optional, Union, Sequence, Type, TypeVar, Any
import os.path
from google.oauth2 import service_account  # type: ignore
import googleapiclient.errors  # type: ignore
import googleapiclient.discovery  # type: ignore
import json


class SchemaError(Exception):
    """Improperly formatted data to deserialize"""


class SchemaColumn:
    name: str
    old_name: str = ""

    def __init__(
            self,
            *,
            line: str,
    ):
        parts = line.split("~", maxsplit=2)
        self.name = parts[0]
        if len(parts) > 1:
            self.old_name = parts[1]

    def debug(
            self
    ):
        if self.old_name:
            return f"{self.old_name} -> {self.name}"
        else:
            return self.name


class SchemaTab:
    name: str
    columns: List[SchemaColumn]

    def __init__(
            self,
            *,
            line: str,
    ):
        parts = line.split(":", maxsplit=2)
        if len(parts) < 2:
            raise SchemaError(
                f"Invalid schema definition. '{line}' should be in the format: 'tabname:col1,col2,col3~oldcol3'")
        self.name = parts[0]
        self.columns = []
        columns = parts[1].split(",")
        if len(columns) < 1:
            raise SchemaError(f"{self.name} has no valid columns defined in '{parts[1]}'")
        for col in columns:
            if not col:
                continue
            self.columns.append(SchemaColumn(line=col))

    def debug(
            self
    ):
        result = f"{self.name} has {len(self.columns)} columns:"
        for col in self.columns:
            result += f"\n\t{col.debug()}"
        return result

    def analyze(self):
        """Compare the schema and the tab, returning delta"""
        pass

    def update(self):
        """Update the tab to match the schema"""
        pass


# @attr.s(auto_attribs=True, kw_only=True)
class SchemaSheet:
    tabs: List[SchemaTab]

    def __init__(
            self,
            *,
            filename: str = "",
            lines: str = "",
    ):
        # Read contents from the file if the schema filename is passed and exists
        if filename:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    lines = f.read()
            else:
                raise SchemaError(f"{filename} was not found or could not be opened for reading")

        parts = lines.split("\n")
        self.tabs = []
        for line in parts:
            if not line:
                continue
            self.tabs.append(SchemaTab(line=line))

    def debug(self):
        result = f"{len(self.tabs)} tabs:"
        for tab in self.tabs:
            result += f"\n{tab.debug()}"
        return result

    def compare(self, schema: "SchemaSheet"):
        pass


def sheet_range_header(tab_name: str):
    return f"{tab_name}!1:1"


class SchemaReader:
    """Reads the schema of any GSheet"""
    schema: SchemaSheet
    spreadsheet_id: str
    credentials: service_account.credentials
    service: googleapiclient.discovery
    tab_names: List[str]
    client: Any

    def __init__(self, *, spreadsheet_id: str, cred_file: str):
        scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets",
        ]

        self.credentials = service_account.Credentials.from_service_account_file(
            cred_file, scopes=scopes
        )

        self.service = googleapiclient.discovery.build(
            "sheets", "v4", credentials=self.credentials, cache_discovery=False
        )
        self.spreadsheet_id = spreadsheet_id
        self.client = self.service.spreadsheets().values()
        lines = self.read_tabs()
        self.schema = SchemaSheet(lines=lines)

    def read_tabs(self):
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        properties = sheet_metadata.get('sheets')
        self.tab_names = []
        lines = ""
        for item in properties:
            title = item.get("properties").get('title')
            self.tab_names.append(title)
            fields = ",".join(self.header_row(title))
            lines += f"{title}:{fields}\n"
        return lines

    def header_row(self, tab_name: str):
        try:
            response = self.client.get(
                spreadsheetId=self.spreadsheet_id, range=sheet_range_header(tab_name)
            ).execute()
        except googleapiclient.errors.HttpError as ex:
            raise SchemaError(str(ex))
        return response["values"][0]

    def debug(self):
        return self.schema.debug()


if __name__ == "__main__":
    schema = SchemaSheet(filename="hackathon.schema")
    print(schema.debug())
