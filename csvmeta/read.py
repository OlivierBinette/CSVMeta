import csv
import json
import os
from typing import Iterable, Union

from csvmeta.write import DEFAULT_DIALECT


def read(dirpath: str) -> Iterable[Iterable[str]]:
    """
    Read CSV data from the specified directory path.

    If specified, the dialect from the metadata file will be used for parsing the CSV file.

    Parameters
    ----------
    dirpath : str
        The directory path containing the CSV file `data.csv` and its metadata file `metadata.json`.

    Returns
    -------
    Iterable[Iterable[str]]
        An iterable of rows, where each row is an iterable of string values. The header is always returned as the first row.
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
    with open(metadata_filepath, newline="") as metafile:
        metadata = json.load(metafile)
    return metadata
