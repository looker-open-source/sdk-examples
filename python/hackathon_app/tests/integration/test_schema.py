import datetime
from typing import Sequence

from schema import SchemaSheet, SchemaTab, SchemaColumn
from sheets import Sheets


def test_read_schema(sheets: Sheets, test_schema):
    """SchemaSheet should read parse all schema."""
    schema = SchemaSheet(gsheet=sheets, contents=test_schema)
    assert isinstance(schema, SchemaSheet)
    assert len(schema.tabs) > 0
