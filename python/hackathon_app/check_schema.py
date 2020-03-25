import sheets
import schema
import os
from tests import conftest


def compare_schema(test: str, expected: schema.SchemaSheet, actual: schema.SchemaSheet):
    delta = expected.compare(actual)
    diff = "\n".join(
        [d.debug() for d in delta if d.diff != schema.Difference.OldName and d.diff != schema.Difference.Columns]
    )
    if len(diff) > 0:
        status = "MISMATCH: "
    else:
        status = "SAME: "
    print(f"\n{status}{test}")
    if len(diff) > 0:
        print(diff)


if __name__ == "__main__":
    print("Checking various schemas. Please wait ...")
    master = schema.SchemaSheet(filename="hackathon.schema")
    model = sheets.get_model_schema()
    files_to_import = conftest.get_tsv_files()
    imported = schema.SchemaSheet(lines="\n".join(schema.import_schema(files_to_import)))
    compare_schema("hackathon.schema vs. code", master, model)
    compare_schema("hackathon.schema vs. imported files", master, imported)
    compare_schema("code vs. imported files", model, imported)
    sheets_to_check = os.getenv("SHEETS_TO_CHECK", "")
    sheet_ids = sheets_to_check.split(",")
    if not sheets_to_check:
        print("To check live Google sheets, export SHEETS_TO_CHECK=sheetId1,sheetId2,...")
    else:
        print(f"Checking {len(sheet_ids)} live sheets {sheets_to_check} ...")


