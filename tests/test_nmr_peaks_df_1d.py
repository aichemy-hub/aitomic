import os

import polars as pl

from aitomic import bruker, nomad_nmr


def test_nmr_peaks_df_1d() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    experiments = client.auto_experiments()
    peak_df = bruker.nmr_peaks_df_1d(experiments.download())
    peak_df = nomad_nmr.add_metadata(client, peak_df)
    peak_df = peak_df.filter(pl.col("username") == "test1").unique("spectrum")
    assert len(peak_df) == 2  # noqa: PLR2004
