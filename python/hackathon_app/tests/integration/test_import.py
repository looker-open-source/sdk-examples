from pprint import pprint
import json
import schema
import pytest
import os
import pathlib


@pytest.fixture(name="tsv_files", scope="session")
def get_tsv_files():
    path = "tests/data"
    files = [f"{path}/{f}" for f in os.listdir(path) if pathlib.Path(f).suffix == ".tsv"]
    return files


@pytest.fixture(name="sheet_names", scope="session")
def get_sheet_names():
    files = [f for f in os.listdir("tests/data") if pathlib.Path(f).suffix == ".tsv"]
    # get the base name of the file without the path
    names = [os.path.splitext(pathlib.PurePath(f).name)[0] for f in files]
    return names


def test_tsv_files(tsv_files):
    assert len(tsv_files) > 0


def test_sheet_names(sheet_names):
    assert len(sheet_names) > 0


def test_import_row_data(tsv_files):
    filename = tsv_files[0]
    data = schema.import_row_data(filename)
    assert len(data) > 0


def test_import_sheet(tsv_files, sheet_names):
    info = schema.import_sheet_data(tsv_files)
    # output = json.dumps(info, indent=2)
    # with open("tests/data/imported.json", "w") as f:
    #     f.write(output)
    assert len(info["sheets"]) == len(sheet_names)
