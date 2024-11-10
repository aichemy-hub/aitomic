"""Generate a data frame from a zip file of Bruker NMR spectra."""

# ruff: noqa: T201
import argparse
from pathlib import Path

import polars as pl

from aitomic import bruker


def main() -> None:
    """Run the example."""
    args = _parse_args()
    pl.Config.set_fmt_str_lengths(1000)
    pl.Config.set_tbl_cols(-1)
    pl.Config.set_tbl_rows(-1)
    peak_df = bruker.nmr_peaks_df_1d(
        args.zip_file.read_bytes(),
        peak_threshold=args.peak_threshold,
    )
    print(peak_df)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a data frame from a zip file of Bruker NMR spectra."
        ),
    )
    parser.add_argument(
        "zip_file",
        type=Path,
        help="The path to the zip file containing Bruker spectra.",
    )
    parser.add_argument(
        "--peak-threshold",
        default=1e4,
        type=float,
        help="Minimum peak height for positive peaks.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
