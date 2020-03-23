from typing import List

import schema
import sheets


def check_delta(test: str, delta: List[schema.Delta]):
    diff = "\n".join(
        [d.debug() for d in delta if d.diff != schema.Difference.OldName and d.diff != schema.Difference.Columns]
    )
    if len(diff) > 0:
        print(f"\n{test}")
        print(diff)


def test_parse_schema(test_schema):
    """SchemaSheet should parse all schema."""
    test_schema = test_schema.strip()
    actual = schema.SchemaSheet(lines=test_schema)
    assert isinstance(actual, schema.SchemaSheet)
    assert len(actual.tabs) > 0
    lines = actual.to_lines()
    assert test_schema == lines


def test_to_lines():
    line = "tab:col1,col2~old2"
    tab = schema.SchemaTab(line=line)
    lines = tab.to_lines()
    assert line == lines


def test_model_compare(test_schema):
    """SchemaSheet should compare all schema."""
    model = sheets.get_model_schema()
    actual = schema.SchemaSheet(lines=test_schema)
    delta = actual.compare(model)
    check_delta("Schema vs. Model", delta)
    assert len(delta) == 0


def test_sheet_compare(create_test_sheet, cred_file, test_schema):
    """SchemaSheet should read parse all schema."""
    spreadsheet_id = create_test_sheet["spreadsheetId"]
    reader = schema.SchemaReader(spreadsheet_id=spreadsheet_id, cred_file=cred_file)
    actual = schema.SchemaSheet(lines=test_schema)
    model = sheets.get_model_schema()
    delta = actual.compare(reader.schema)
    url = create_test_sheet["spreadsheetUrl"]
    check_delta(f"Schema vs. Sheet {url}", delta)
    delta2 = model.compare(reader.schema)
    check_delta(f"Model vs. Sheet {url}", delta2)
    assert len(delta) == 0
    assert len(delta2) == 0
