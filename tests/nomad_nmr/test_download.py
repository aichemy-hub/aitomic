import os
import tempfile
import zipfile

import polars as pl

from aitomic import bruker, nomad_nmr


def test_download_all() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    experiments = client.auto_experiments()
    spectra = (
        bruker.nmr_peaks_df_1d(experiments.download())
        .select("spectrum")
        .unique()
        .sort("spectrum")
    )
    pl.Config.set_fmt_str_lengths(1000)
    pl.Config.set_tbl_cols(-1)
    pl.Config.set_tbl_rows(-1)
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
    with tempfile.NamedTemporaryFile("wb") as f:
        f.write(experiments.download())
        f.seek(0)

        expected_files = sorted(
            [
                "2106231050-2-1-test1-10.json",
                "2106231050-2-1-test1-11.json",
                "2106241100-10-2-test3-10.json",
            ]
        )
        with zipfile.ZipFile(f.name) as zip_file:
            files = sorted(zip_file.namelist())
            assert files == expected_files
            for file in files:
                assert (
                    zip_file.read(file).decode()
                    == f'"{file.removesuffix(".json")}"'
                )
