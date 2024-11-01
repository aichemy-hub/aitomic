"""Tools to interact with NOMAD NMR.

A `NOMAD NMR`_ deployment is used by NMR labs to manage their machines
and store their data in a central place and in a
`FAIR <https://en.wikipedia.org/wiki/FAIR_data>`_ manner. It automatically
provides features such as a monitoring system and a data repository which
includes metadata and access control.

The NOMAD NMR `server <https://github.com/nomad-nmr/nomad-server>`_ provides a
REST API to interact with it, which this module relies upon. The primary goal
of this module is to provide an interface for downloading large datasets from
the NOMAD server and turn them into data frames which can be used for
machine learning.

.. _`NOMAD NMR`: https://www.nomad-nmr.uk

Examples:
    .. _downloading-experiment-data:

    **Downloading experiment data**

    .. testsetup:: downloading-experiment-data

        from aitomic import nomad_nmr
        import tempfile
        import os

        tmp = tempfile.TemporaryDirectory()
        pwd = os.getcwd()
        os.chdir(tmp.name)

        def change_url(func):
            def wrapper(url, username, password):
                return func(
                    os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
                    username="admin",
                    password="foo",
                )
            return wrapper

        nomad_nmr.Client.login = change_url(nomad_nmr.Client.login)

    .. testcode:: downloading-experiment-data

        from aitomic import nomad_nmr
        from pathlib import Path

        client = nomad_nmr.Client.login(
            "http://demo.nomad-nmr.uk",
            username="demo",
            password="dem0User",
        )
        experiments = client.auto_experiments()
        Path("experiments.zip").write_bytes(experiments.download())

    .. testcleanup:: downloading-experiment-data

        os.chdir(pwd)


    .. _downloading-experiment-data-query:

    **Downloading experiment data matching a query**

    .. testsetup:: downloading-experiment-data-query

        from aitomic import nomad_nmr
        import tempfile
        import os

        tmp = tempfile.TemporaryDirectory()
        pwd = os.getcwd()
        os.chdir(tmp.name)

        def change_url(func):
            def wrapper(url, username, password):
                return func(
                    os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
                    username="admin",
                    password="foo",
                )
            return wrapper

        nomad_nmr.Client.login = change_url(nomad_nmr.Client.login)

    .. testcode:: downloading-experiment-data-query

        from aitomic import nomad_nmr
        from pathlib import Path

        client = nomad_nmr.Client.login(
            "http://demo.nomad-nmr.uk",
            username="demo",
            password="dem0User",
        )
        experiments = client.auto_experiments(
            query=nomad_nmr.AutoExperimentQuery(
                solvent="DMSO",
                title=["test", "test-1"]
            )
        )
        Path("experiments.zip").write_bytes(experiments.download())
"""

from aitomic._internal.nomad_nmr import (
    AuthToken,
    AutoExperiment,
    AutoExperimentQuery,
    AutoExperiments,
    Client,
)

__all__ = [
    "AuthToken",
    "AutoExperiment",
    "AutoExperimentQuery",
    "AutoExperiments",
    "Client",
]
