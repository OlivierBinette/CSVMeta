import csv
import json
import os
from typing import Any, Iterable, Optional

DEFAULT_DIALECT = "unix"


def write(
    dirpath: str,
    rowsdata: Iterable[Iterable[Any]],
    schema: Optional[dict] = None,
    header: bool = False,
    dialect: str | dict = DEFAULT_DIALECT,
    **additional_metadata
) -> None:
    """
    Write CSV data and optional metadata.

    Parameters
    ----------
    dirpath : str
        The directory path where the CSV file and metadata will be saved.
    rowsdata : Iterable[Iterable[Any]]
        The data to be written to the CSV file.
    schema : Optional[dict], optional
        The schema definition for the data, by default None.
    header : bool, optional
        Flag to indicate if the first row of the data is a header, by default True.
    dialect : str | dict, optional
        The dialect to be used for writing the CSV file, by default DEFAULT_DIALECT (unix). See https://docs.python.org/3/library/csv.html#csv-fmt-params for valid parameters and more information.
    additional_metadata : dict, optional
        Additional metadata to be written to the metadata file.
    """
    _write_csv(dirpath, rowsdata, dialect)
    _write_metadata(dirpath, schema, header, dialect, **additional_metadata)


def _write_csv(dirpath: str, rowsdata: Iterable[Iterable[Any]], dialect: str | dict = DEFAULT_DIALECT) -> None:
    """
    Internal function to write data to a CSV file.

    Parameters
    ----------
    dirpath : str
        The directory path where the CSV file will be saved.
    rowsdata : Iterable[Iterable[Any]]
        The data to be written to the CSV file.
    header : bool, optional
        Flag to indicate if the first row of the data is a header, by default True.
    dialect : str | dict, optional
        The dialect to be used for writing the CSV file, by default DEFAULT_DIALECT.
    """
    csv_filepath = os.path.join(dirpath, "data.csv")
    with open(csv_filepath, "w", newline="") as csvfile:
        if isinstance(dialect, str):
            writer = csv.writer(csvfile, dialect=dialect)
        else:
            writer = csv.writer(csvfile, **dialect)

        for row in rowsdata:
            writer.writerow(row)


def _write_metadata(
    dirpath: str, schema: Optional[dict] = None, header: bool = False, dialect: str | dict = DEFAULT_DIALECT, **additional_metadata) -> None:
    """
    Internal function to write metadata associated with a CSV file.

    Parameters
    ----------
    dirpath : str
        The directory path where the metadata will be saved.
    schema : Optional[dict], optional
        The schema definition for the data, by default None.
    header : bool, optional
        Flag to indicate if the first row of the data is a header, by default True.
    dialect : str | dict, optional
        The dialect used for the CSV file, by default DEFAULT_DIALECT.
    additional_metadata : dict, optional
        Additional metadata to be written to the metadata file.
    """
    metadata = {"schema": schema, "header": header, "dialect": dialect}
    metadata.update(additional_metadata)

    metadata_filepath = os.path.join(dirpath, "metadata.json")
    with open(metadata_filepath, "w") as metafile:
        json.dump(metadata, metafile, indent=4)
