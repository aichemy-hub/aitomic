import os
import tempfile
import zipfile

from aitomic import nomad_nmr


def test_download_all() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    experiments = client.auto_experiments()
    with tempfile.NamedTemporaryFile("wb") as f:
        f.write(experiments.download())
        f.seek(0)

        expected_files = sorted(
            [
                "2106231050-2-1-test1-10.json",
                "2106231050-2-1-test1-11.json",
                "2106231055-3-2-test2-10.json",
                "2106231100-10-2-test3-10.json",
                "2106240012-10-2-test2-10.json",
                "2106241100-10-2-test3-10.json",
                "2106241100-10-2-test4-1.json",
            ]
        )
        assert len(experiments) == len(expected_files)
        with zipfile.ZipFile(f.name) as zip_file:
            files = sorted(zip_file.namelist())
            assert files == expected_files
            for file in files:
                assert (
                    zip_file.read(file).decode()
                    == f'"{file.removesuffix(".json")}"'
                )


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
