from typing import Dict, Generic, List, Optional, Union, Sequence, Type, TypeVar
import datetime
import itertools
import re

import attr
import cattr
from google.oauth2 import service_account  # type: ignore
import googleapiclient.errors  # type: ignore
import googleapiclient.discovery  # type: ignore

from sheets import SheetError

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
            return self.old_name + " -> " + self.name
        else:
            return self.name


TSchemaColumn = TypeVar("TSchemaColumn", bound=SchemaColumn)


@attr.s(auto_attribs=True, kw_only=True)
class SchemaColumns(Generic[TSchemaColumn]):
    def __init__(
            self,
            *,
            line: str
    ):
        parts = line.split(',')
        for part in parts:
            # TODO how do I add a column to SchemaColumns self?
            self.append(SchemaColumn(part))

    def debug(
            self
    ):
        # TODO want to dump all columns on a new line
        result = self.count() + " columns:"
        for item in self:
            result += "\n\t" + item.debug()
        return result


@attr.s(auto_attribs=True, kw_only=True)
class SchemaTab:
    name: str
    columns: SchemaColumns

    def __init__(
            self,
            *,
            line: str,
    ):
        parts = line.split(":", maxsplit=2)
        if parts.count() < 2:
            raise SheetError("Invalid schema definition. Should be in the format: 'tabname:col1,col2,col3~oldcol3'")
        self.name = parts[0]
        self.columns = SchemaColumns(parts[1])

    def debug(
            self
    ):
        return self.name + " has " + self.columns.debug()

