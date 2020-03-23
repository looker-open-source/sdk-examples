import enum
import difflib
from typing import Dict, Generic, List, Optional, Union, Sequence, Type, TypeVar, Any
import os.path
from google.oauth2 import service_account  # type: ignore
import googleapiclient.errors  # type: ignore
import googleapiclient.discovery  # type: ignore


def sheet_range_header(tab_name: str):
    """Returns the sheet range for the header row of a named tab"""
    return f"{tab_name}!1:1"


class Difference(enum.Enum):
    """Comparison differences"""
    Position = enum.auto()  # Position is different
    Name = enum.auto()  # Name is different
    OldName = enum.auto()  # Old name is different
    Columns = enum.auto()  # Column definitions differ
    Missing = enum.auto()  # Item is not found in "other"


class Delta:
    name: str = ""
    old_name: str = ""
    position: int = 0
    old_position: int = 0
    diff: Difference

    def __init__(
            self,
            *,
            name: str = "",
            old_name: str = "",
            position: int = 0,
            old_position: int = 0,
            diff,
    ):
        self.name = name
        self.old_name = old_name
        self.position = position
        self.old_position = old_position
        self.diff = diff

    def debug(self):
        result = ""
        if Difference.Position in self.diff:
            # This can only be set for columns
            result += f"{self.column_name} position is {self.old_position}, not {self.position}. "
        if Difference.Name in self.diff:
            result += f"'Name {self.old_name}' has been changed to '{self.name}'. "
        if Difference.OldName in self.diff:
            result += f"Old Name '{self.old_name}' has been changed to '{self.name}'. "
        if Difference.Columns in self.diff:
            result += f"Columns for tab '{self.name}' do not match'. "
        if Difference.Missing in self.diff:
            result += f"'{self.name}' was not found in other. "
        return result


class SchemaError(Exception):
    """Improperly formatted data to deserialize"""


class SchemaName:
    """Base class for sheet schema"""
    name: str = ""
    old_name: str = ""

    def __init__(self, *, name: str):
        parts = name.split("~", maxsplit=2)
        self.name = parts[0]
        if len(parts) > 1:
            self.old_name = parts[1]
        else:
            self.old_name = ""

    def debug(self):
        if self.old_name:
            return f"{self.old_name} -> {self.name}"
        else:
            return self.name

    def compare(self, other: "SchemaName"):
        delta: List[Delta] = []
        if other.name != self.name:
            delta.append(Delta(name=self.name, old_name=other.name, diff=Difference.Name))
        if other.old_name != self.old_name:
            delta.append(Delta(name=self.old_name, old_name=other.old_name, diff=Difference.OldName))
        return delta

    def to_lines(self):
        if self.old_name:
            return f"{self.name}~{self.old_name}"
        return self.name


class SchemaColumn(SchemaName):
    """Sheet column schema object"""
    position: int = 0

    def __init__(self, *, line: str, position: int = 0):
        super().__init__(name=line)
        self.position = position

    def compare(self, other: "SchemaColumn"):
        delta = super().compare(other)
        if other.position != self.position:
            delta.append(
                Delta(name=self.name, old_name=other.old_name, position=self.position, old_position=other.position,
                      diff=Difference.Position))
        return delta


def find_column(name: str, cols: List[SchemaColumn]) -> Union[SchemaColumn, None]:
    try:
        return next(x for x in cols if x.name == name)
    except StopIteration:
        return None


class SchemaTab(SchemaName):
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
        super().__init__(name=parts[0])
        self.columns = []
        columns = parts[1].split(",")
        if len(columns) < 1:
            raise SchemaError(f"{self.name} has no valid columns defined in '{parts[1]}'")
        for index, col in enumerate(columns):
            if not col:
                continue
            self.columns.append(SchemaColumn(line=col, position=index))

    def debug(
            self
    ):
        result = f"{super().debug()} has {len(self.columns)} columns:"
        for col in self.columns:
            result += f"\n\t{col.debug()}"
        return result

    def compare(self, other: "SchemaTab"):
        """Compare the schema and the tab, returning delta"""
        delta = super().compare(other)
        colDiff = False
        for col in self.columns:
            col2 = find_column(col.name, other.columns)
            if col2:
                diffs = col.compare(col2)
                if len(diffs) > 0:
                    colDiff = True
                    for d in diffs:
                        delta.append(d)
            else:
                colDiff = True
                delta.append(Delta(name=col.name, diff=Difference.Missing))

        if colDiff:
            delta.append(Delta(name=self.name, diff=Difference.Columns))
        return delta

    def to_lines(self):
        names = [c.to_lines() for c in self.columns]
        fields = ",".join(names)
        lines = f"{super().to_lines()}:{fields}"
        return lines

    def update(self):
        """Update the tab to match the schema"""
        pass


def find_tab(name: str, tabs: List[SchemaTab]) -> Union[SchemaTab, None]:
    try:
        return next(x for x in tabs if x.name == name)
    except StopIteration:
        return None


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

    def compare(self, other: "SchemaSheet"):
        delta: List[Delta] = []
        for index, t in enumerate(self.tabs):
            t2 = find_tab(t.name, other.tabs)
            if t2:
                diff = t.compare(t2)
                if len(diff) > 0:
                    for d in diff:
                        delta.append(d)
            else:
                delta.append(Delta(name=t.name, diff=Difference.Missing))
        return delta

    def to_lines(self):
        lines = [t.to_lines() for t in self.tabs]
        return "\n".join(lines).strip()

    def whats_the_diff(self, other: "SchemaSheet", html: bool = False):
        lines = self.to_lines()
        other_lines = other.to_lines()
        if html:
            differ = difflib.HtmlDiff()
            result = differ.make_table(fromlines=lines, tolines=other_lines)
        else:
            differ = difflib.Differ()
            result = differ.compare(lines, other_lines)
        return result


class DiffColumn:
    expected: SchemaColumn
    actual: SchemaColumn
    delta: List[Delta]

    def __init__(
            self,
            *,
            expected: SchemaColumn,
            actual: SchemaColumn,
    ):
        self.delta = expected.compare(actual)


class DiffTab:
    tab: str = ""
    delta = List[Delta]

    def __init__(
            self,
            *,
            expected: SchemaTab,
            actual: SchemaTab,
    ):
        self.delta = expected.compare(actual)


class DiffSchema:
    delta: List[Delta]

    def __init__(
            self,
            *,
            expected: SchemaSheet,
            actual: SchemaSheet,
    ):
        self.delta = expected.compare(actual)


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
