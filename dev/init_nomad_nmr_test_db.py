"""Populate a test NOMAD NMR database with data."""

import argparse
from pathlib import Path
from typing import Any

import pymongo
from pydantic import BaseModel


def main() -> None:
    """Run the example."""
    args = _parse_args()

    client = pymongo.MongoClient[Any](args.uri)
    db = client.get_database("nomad")
    instruments = _add_instruments(db)


class Instrument(BaseModel):
    """An instrument."""


def _add_instruments(db: pymongo.database.Database) -> list[Instrument]:
    pass


def _parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Populate a test NOMAD NMR database with data."
    )
    parser.add_argument(
        "uri",
        help="The URI of the NOMAD server.",
    )
    parser.add_argument(
        "datastore",
        help="The path to the NOMAD datastore.",
        type=Path,
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
