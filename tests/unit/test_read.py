import csv
import json
import os

from bettercsv import metadata, read, schema


def test_read_csv(tmpdir, example_csv_data, example_metadata, dialect):
    """
    Test the read function for correct CSV reading and dialect handling.
    """
    dirpath = tmpdir.strpath
    csv_filepath = os.path.join(dirpath, "data.csv")
    metadata_filepath = os.path.join(dirpath, "metadata.json")

    # Create a sample CSV file and metadata file in the temporary directory
    with open(csv_filepath, "w", newline="") as csvfile:
        if isinstance(dialect, str):
            writer = csv.writer(csvfile, dialect=dialect)
        else:
            writer = csv.writer(csvfile, **dialect)
        writer.writerows(example_csv_data)

    with open(metadata_filepath, "w") as metafile:
        meta = example_metadata.copy()
        meta["dialect"] = dialect
        json.dump(meta, metafile)

    # Call the read function
    result = list(read(dirpath))

    # Verify the read data matches the example data
    for expected_row, row in zip(example_csv_data, result):
        assert list(row) == expected_row


def test_metadata(tmpdir, example_metadata):
    """
    Test the metadata function for correct metadata reading.
    """
    dirpath = tmpdir.strpath
    metadata_filepath = os.path.join(dirpath, "metadata.json")

    # Create a sample schema file in the temporary directory
    with open(metadata_filepath, "w") as meta:
        json.dump(example_metadata, meta)

    # Call the schema function
    result_metadata = metadata(dirpath)

    # Verify the read schema matches the example schema
    assert result_metadata == example_metadata


def test_schema(tmpdir, example_metadata):
    """
    Test the schema function for correct schema reading.
    """
    dirpath = tmpdir.strpath
    metadata_filepath = os.path.join(dirpath, "metadata.json")

    # Create a sample schema file in the temporary directory
    with open(metadata_filepath, "w") as metadata:
        json.dump(example_metadata, metadata)

    # Call the schema function
    result_schema = schema(dirpath)

    # Verify the read schema matches the example schema
    assert result_schema == example_metadata.get("schema")
