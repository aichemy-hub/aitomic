import os

import polars as pl

from aitomic import bruker, nomad_nmr


def test_download_all() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    experiments = client.auto_experiments()
    assert len(experiments) == 5  # noqa: PLR2004
    spectra = (
        bruker.nmr_peaks_df_1d(experiments.download())
        .select("spectrum")
        .unique()
        .sort("spectrum")
    )
    expected = pl.DataFrame(
        {
            "spectrum": [
                "2409231309-0-2-lukasturcani/10/pdata/1",
                "2409231309-0-3-lukasturcani/10/pdata/1",
                "2410081201-0-1-lukasturcani/10/pdata/1",
                "2410161546-0-1-admin/10/pdata/1",
            ]
        }
    ).sort("spectrum")
    assert spectra.equals(expected)


def test_download_some() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    experiments = client.auto_experiments(
        nomad_nmr.AutoExperimentQuery(
            solvent="CDCl3", title=["Test Exp 1", "Test Exp 6"]
        )
    )
    spectra = (
        bruker.nmr_peaks_df_1d(experiments.download())
        .select("spectrum")
        .unique()
        .sort("spectrum")
    )
    expected = pl.DataFrame(
        {
            "spectrum": [
                "2409231309-0-2-lukasturcani/10/pdata/1",
                "2410161546-0-1-admin/10/pdata/1",
            ]
        }
    ).sort("spectrum")
    assert spectra.equals(expected)
