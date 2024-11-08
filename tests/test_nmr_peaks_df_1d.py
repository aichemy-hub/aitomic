import os

from aitomic import bruker, nomad_nmr


def test_nmr_peaks_df_1d() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    experiments = client.auto_experiments()
    peak_df = bruker.nmr_peaks_df_1d(experiments.download())
    peakd_df = nomad_nmr.add_metadata(client, peak_df)
    print(peakd_df)
    assert False
