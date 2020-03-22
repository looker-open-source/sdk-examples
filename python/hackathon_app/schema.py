from typing import Dict, Generic, List, Optional, Union, Sequence, Type, TypeVar
import os.path

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

        lines = lines.split("\n")
        self.tabs = []
        for line in lines:
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

if __name__ == "__main__":
    schema = SchemaSheet(filename="hackathon.schema")
    print(schema.debug())
