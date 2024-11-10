"""Generate a peak data frame from data stored in NOMAD NMR."""

# ruff: noqa: T201
import argparse

import polars as pl

from aitomic import bruker, nomad_nmr


def main() -> None:
    """Run the example."""
    pl.Config.set_fmt_str_lengths(1000)
    pl.Config.set_tbl_cols(-1)
    pl.Config.set_tbl_rows(-1)

    args = _parse_args()
    client = nomad_nmr.Client.login(
        args.nomad_nmr_url,
        username=args.username,
        password=args.password,
    )
    peak_df = bruker.nmr_peaks_df_1d(client.auto_experiments().download())
    peak_df = nomad_nmr.add_metadata(client, peak_df)
    print(peak_df)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a peak data frame from data stored in NOMAD NMR."
    )
    parser.add_argument(
        "--nomad-nmr-url",
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
    return parser.parse_args()


if __name__ == "__main__":
    main()
