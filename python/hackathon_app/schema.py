from typing import Dict, Generic, List, Optional, Union, Sequence, Type, TypeVar
import os.path
import datetime
import itertools
import re

import attr
import cattr
from google.oauth2 import service_account  # type: ignore
import googleapiclient.errors  # type: ignore
import googleapiclient.discovery  # type: ignore

from sheets import SheetError, Sheets

# TODO get lots of syntax help in this file!!!


@attr.s(auto_attribs=True, kw_only=True)
class SchemaColumn:
    name: str
    old_name: str = None

    def __init__(
            self,
            *,
            line: str,
    ):
        parts = line.split("~", maxsplit=2)
        self.name = parts[0]
        if parts.count() > 1:
            self.old_name = parts[1]

    def debug(
            self
    ):
        if self.old_name is not None:
            return f"{self.old_name } -> {self.name}"
        else:
            return self.name


# TSchemaColumn = TypeVar("TSchemaColumn", bound=SchemaColumn)


# TODO should this be a List, Array, or what? I'd like to use it instead of [SchemaColumn] in SchemaTab.
#  but maybe it's not worth the bother?
# @attr.s(auto_attribs=True, kw_only=True)
# class SchemaColumns(Generic[TSchemaColumn]):
#     def __init__(
#             self,
#             *,
#             line: str
#     ):
#         parts = line.split(',')
#         for part in parts:
#             # TODO how do I add a column to SchemaColumns self?
#             self.append(SchemaColumn(line=part))
#
#     def debug(
#             self
#     ):
#         # TODO want to dump all columns on a new line
#         result = f"{self.count()} columns:"
#         for item in self:
#             result += f"\n\t{item.debug()}"
#         return result


@attr.s(auto_attribs=True, kw_only=True)
class SchemaTab:
    name: str
    columns: [SchemaColumn]

    def __init__(
            self,
            *,
            line: str,
    ):
        parts = line.split(":", maxsplit=2)
        if parts.count() < 2:
            raise SheetError("Invalid schema definition. Should be in the format: 'tabname:col1,col2,col3~oldcol3'")
        self.name = parts[0]
        self.columns = []
        columns = parts[1].split(",")
        if columns.count() < 1:
            raise SheetError(f"{self.name} has no valid columns defined in '{parts[1]}'")
        for col in columns:
            self.columns.append(SchemaColumn(line=col))

    def debug(
            self
    ):
        result = f"{self.name} has {self.columns.count()} columns:"
        for col in self.columns:
            result += f"\n\t{col.debug()}"
        return result

    def analyze(self):
        """Compare the schema and the tab, returning delta"""
        pass

    def update(self):
        """Update the tab to match the schema"""
        pass


@attr.s(auto_attribs=True, kw_only=True)
class SchemaSheet:
    sheet: Sheets
    tabs: [SchemaTab]

    def __init__(
            self,
            *,
            gsheet: Sheets = None,
            filename: str = "",
            contents: str = "",
    ):
        self.sheet = gsheet
        # Read contents from the file if the schema filename is passed and exists
        if filename:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    contents = f.read()
            else:
                raise SheetError(f"{filename} was not found or could not be opened for reading")

        if not contents:
            raise SheetError(f"No contents to process in {filename}")

        lines = contents.split("\n")
        self.tabs = []
        for line in lines:
            self.tabs.append(SchemaTab(line=line))

    def debug(self):
        result = f"{self.tabs.count()} tabs:\n"
        for tab in self.tabs:
            result += tab.debug()


if __name__ == "__main__":
    schema = SchemaSheet(filename="hackathon.schema")
    print(schema.debug())
