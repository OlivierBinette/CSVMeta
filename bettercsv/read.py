import csv
import json
import os
from typing import Iterable, Union

from bettercsv.write import DEFAULT_DIALECT


def read(dirpath: str) -> Iterable[Iterable[str]]:
    """
    Read CSV data from the specified directory path.

    Parameters
    ----------
    dirpath : str
        The directory path containing the CSV file and its metadata.

    Returns
    -------
    Iterable[Iterable[str]]
        An iterable of rows, where each row is an iterable of string values.
    """
    meta = metadata(dirpath)
    dialect = meta.get("dialect", DEFAULT_DIALECT)

    reader = _read_csv(dirpath, dialect)

    return reader


def _read_csv(dirpath: str, dialect: Union[str, dict]) -> Iterable[Iterable[str]]:
    """
    Internal function to read a CSV file using the specified dialect.

    Parameters
    ----------
    dirpath : str
        The directory path containing the CSV file.
    dialect : str | dict
        The CSV dialect to use for parsing.

    Returns
    -------
    Iterable[Iterable[str]]
        An iterable of rows, where each row is an iterable of string values.
    """
    csv_filepath = os.path.join(dirpath, "data.csv")
    with open(csv_filepath, newline="") as csvfile:
        if isinstance(dialect, str):
            reader = csv.reader(csvfile, dialect=dialect)
        else:
            reader = csv.reader(csvfile, **dialect)
        for row in reader:
            yield row


def metadata(dirpath: str) -> dict:
    """
    Read the metadata associated with a CSV file.

    Parameters
    ----------
    dirpath : str
        The directory path containing the metadata file.

    Returns
    -------
    dict
        A dictionary of metadata key-value pairs.
    """
    metadata_filepath = os.path.join(dirpath, "metadata.json")
    with open(metadata_filepath, "r") as metafile:
        metadata = json.load(metafile)
    return metadata


def schema(dirpath: str) -> dict:
    """
    Read the schema of the CSV file from the specified directory path.

    Parameters
    ----------
    dirpath : str
        The directory path containing the schema information.

    Returns
    -------
    dict
        A dictionary representing the schema of the CSV file.
    """
    schema_filepath = os.path.join(dirpath, "metadata.json")
    with open(schema_filepath, "r") as metadata:
        metadata = json.load(metadata)
    return metadata.get("schema", None)
