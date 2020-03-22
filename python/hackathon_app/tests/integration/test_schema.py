
import schema
import sheets


# def test_read_schema(sheets: Sheets, test_schema):
def test_read_schema(test_schema):
    """SchemaSheet should read parse all schema."""
    actual = schema.SchemaSheet(lines=test_schema)
    assert isinstance(actual, schema.SchemaSheet)
    assert len(actual.tabs) > 0


def test_schema_compare(test_schema):
    """SchemaSheet should read parse all schema."""
    code = sheets.get_sheet_schema()
    actual = schema.SchemaSheet(lines=test_schema)
    assert isinstance(code, schema.SchemaSheet)
    assert isinstance(actual, schema.SchemaSheet)
    assert len(actual.tabs) > 0

def test_schema_reader(spreadsheet_id, credentials):
    """SchemaSheet should read parse all schema."""
    code = sheets.get_sheet_schema()
    actual = schema.SchemaSheet(lines=test_schema)
    assert isinstance(code, schema.SchemaSheet)
    assert isinstance(actual, schema.SchemaSheet)
    assert len(actual.tabs) > 0

