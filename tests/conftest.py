import csv

import pytest

DIALECTS_LIST = [
    "excel",
    "unix",
    {"delimiter": "|", "escapechar": "\\", "quotechar": "'", "quoting": csv.QUOTE_NONE, "lineterminator": "\n"},
    {
        "delimiter": ",",
        "doublequote": True,
        "lineterminator": "\r\n",
        "quotechar": '"',
        "quoting": 0,  # Minimal quoting
        "skipinitialspace": False,
        "strict": True,
    },
]


@pytest.fixture(params=DIALECTS_LIST, ids=[str(d) for d in DIALECTS_LIST])
def dialect(request):
    return request.param


@pytest.fixture
def example_rowsdata():
    # Return example data rows
    return [["Header1", "Header2"], ["Value1", "Value2"], ["Value3", "Value4"]]


@pytest.fixture
def example_schema():
    # Return an example schema
    return {"column1": "string", "column2": "string"}


@pytest.fixture
def example_csv_data():
    # Return example CSV data
    return [
        ["Header1", "Header2"],
        ["Value1", None],
        [0, 2 + 3j],
        [True, False],
        [1.0, Exception],
        [dict(a=1, b=2), [3, 4]],
        [{1, "a"}, (1, 2, 3)],
        [csv.Dialect, csv.excel],
    ]


@pytest.fixture
def example_metadata(example_schema):
    # Return an example metadata dictionary
    metadata = {"schema": example_schema, "header": True, "dialect": "excel"}
    return metadata
