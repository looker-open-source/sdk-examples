import datetime
from typing import Sequence

from schema import SchemaSheet, SchemaTab, SchemaColumn
from sheets import Sheets


# def test_read_schema(sheets: Sheets, test_schema):
def test_read_schema(test_schema):
    """SchemaSheet should read parse all schema."""
    schema = SchemaSheet(lines=test_schema)
    assert isinstance(schema, SchemaSheet)
    assert len(schema.tabs) > 0


def test_schema_compare(sheets: Sheets, test_schema):
    """SchemaSheet should read parse all schema."""
    code = sheets.get_schema()
    schema = SchemaSheet(lines=test_schema)
    assert isinstance(code, SchemaSheet)
    assert isinstance(schema, SchemaSheet)
    assert len(schema.tabs) > 0

