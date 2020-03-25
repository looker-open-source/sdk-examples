import sheets
import schema
import os
import sheet_utils


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


def sheet_url(sheet_id: str):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"


if __name__ == "__main__":
    print("Checking various schemas. Please wait ...")
    master = schema.SchemaSheet(filename="hackathon.schema")
    model = sheets.get_model_schema()
    files_to_import = sheet_utils.get_tsv_files()
    imported = schema.SchemaSheet(lines="\n".join(schema.import_schema(files_to_import)))
    compare_schema("hackathon.schema vs. code", master, model)
    compare_schema("hackathon.schema vs. imported files", master, imported)
    compare_schema("code vs. imported files", model, imported)

    # check the schema on any sheets that may have ids specified
    sheets_to_check = os.getenv("GSHEETS_TO_CHECK", "")
    sheet_ids = sheets_to_check.split(",")
    if not sheets_to_check:
        print("\nTo check live Google sheets, export SHEETS_TO_CHECK=sheetId1,sheetId2,...")
    else:
        print(f"\nChecking {len(sheet_ids)} live sheets {sheets_to_check} ...")
        creds = sheet_utils.cred_file()

        for sid in sheet_ids:
            url = sheet_url(sid)
            print(f"Reading {url}")
            reader = schema.SchemaReader(
                spreadsheet_id=sid,
                cred_file=creds,
            )
            compare_schema(f"hackathon.schema vs. {url}", master, reader.schema)


