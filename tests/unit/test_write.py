import csv
import json
import os

from bettercsv import write


def test_write_csv(tmpdir, example_rowsdata, example_schema, dialect):
    """
    Test the write function for correct CSV and metadata output.
    """
    dirpath = tmpdir.strpath

    # Call the write function
    write(dirpath, example_rowsdata, example_schema, True, dialect)

    # Verify CSV file content
    with open(os.path.join(dirpath, "data.csv"), "r") as csvfile:
        if isinstance(dialect, str):
            reader = csv.reader(csvfile, dialect=dialect)
        else:
            reader = csv.reader(csvfile, **dialect)

        for expected_row, row in zip(example_rowsdata, reader):
            assert row == expected_row

    # Verify metadata file content
    with open(os.path.join(dirpath, "metadata.json"), "r") as metafile:
        metadata = json.load(metafile)
        assert metadata["schema"] == example_schema
        assert metadata["dialect"] == dialect
        assert metadata["header"] == True
