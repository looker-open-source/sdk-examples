import datetime
from typing import Sequence

from schema import SchemaSheet, SchemaTab, SchemaColumn
from sheets import Sheets


# def test_read_schema(sheets: Sheets, test_schema):
def test_read_schema(test_schema):
    """SchemaSheet should read parse all schema."""
    schema = SchemaSheet(contents=test_schema)
    assert isinstance(schema, SchemaSheet)
    assert len(schema.tabs) > 0


def test_schema_analyze(sheets: Sheets, test_schema):
    """SchemaSheet should read parse all schema."""
    schema = SchemaSheet(sheet=sheets, contents=test_schema)
    assert isinstance(schema, SchemaSheet)
    assert isinstance(schema.sheet, Sheets)
    assert len(schema.tabs) > 0

