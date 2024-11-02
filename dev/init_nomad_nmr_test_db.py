"""Populate a test NOMAD NMR database with data."""

import argparse
from pathlib import Path

from aitomic import nomad_nmr


def main() -> None:
    """Run the example."""
    args = _parse_args()

    client = nomad_nmr.Client.login(
        args.url,
        username=args.username,
        password=args.password,
    )
    client.auto_experiments().download()


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
