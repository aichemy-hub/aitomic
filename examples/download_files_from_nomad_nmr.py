"""Download files from NOMAD NMR."""

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
    experiments = client.auto_experiments()
    args.download_path.write_bytes(experiments.download())


def _parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download files from NOMAD NMR."
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8080",
        help="The URL of the NOMAD server.",
    )
    parser.add_argument(
        "--username",
        default="admin",
        help="The username to use for authentication.",
    )
    parser.add_argument(
        "--password",
        default="foo",
        help="The password to use for authentication.",
    )
    parser.add_argument(
        "--download-path",
        default=Path("experiments.zip"),
        type=Path,
        help="The path to download the experiments to.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
