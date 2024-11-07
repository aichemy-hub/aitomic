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
    .. _getting-peak-df:

    **Gettiing an NMR peak data frame**

    If you have data in the NOMAD server, chances are you want to use it for
    some kind of data analysis. The easiest thing to do is to get a
    :class:`polars.DataFrame` with all your NMR peaks. Here we produce
    :class:`polars.DataFrame` holding all the peaks, including their
    spectrum of origin, ppm and volume:

    .. testsetup:: getting-peak-df

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

    .. testcode:: getting-peak-df

        from aitomic import bruker, nomad_nmr

        client = nomad_nmr.Client.login(
            "http://demo.nomad-nmr.uk",
            username="demo",
            password="dem0User",
        )
        experiments = client.auto_experiments()
        peak_df = bruker.peaks_df_1d(experiments.download())

    .. testcode:: getting-peak-df
        :hide:

        print(peak_df)

    ::

        ┌────────────────────────────────────────┬───────────┬───────────────┐
        │ spectrum                               ┆ ppm       ┆ volume        │
        │ ---                                    ┆ ---       ┆ ---           │
        │ str                                    ┆ f64       ┆ f64           │
        ╞════════════════════════════════════════╪═══════════╪═══════════════╡
        │ 2410081201-0-1-lukasturcani/10/pdata/1 ┆ 8.344768  ┆ 20680.796875  │
        │ 2410081201-0-1-lukasturcani/10/pdata/1 ┆ 8.339878  ┆ 31792.195312  │
        │ 2410081201-0-1-lukasturcani/10/pdata/1 ┆ 8.338044  ┆ 20503.757812  │
        │ 2410081201-0-1-lukasturcani/10/pdata/1 ┆ 8.336821  ┆ 10042.96875   │
        │ 2410081201-0-1-lukasturcani/10/pdata/1 ┆ 8.323985  ┆ 10558.703125  │
        │ 2410081201-0-1-lukasturcani/10/pdata/1 ┆ 8.317872  ┆ 140601.851562 │
        │ 2410081201-0-1-lukasturcani/10/pdata/1 ┆ 8.307481  ┆ 10210.3125    │

    .. testcleanup:: getting-peak-df

        os.chdir(pwd)

    .. seealso::

        * :func:`.bruker.nmr_peaks_df_1d`: For additional documentation.
        * :meth:`.nomad_nmr.Client.login`: For additional documentation.
        * :meth:`.nomad_nmr.Client.auto_experiments`: For additional
          documentation.
        * :meth:`.nomad_nmr.AutoExperiments.download`: For additional
          documentation.

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

    .. seealso::

        * :meth:`.nomad_nmr.Client.login`: For additional documentation.
        * :meth:`.nomad_nmr.Client.auto_experiments`: For additional
          documentation.
        * :meth:`.nomad_nmr.AutoExperiments.download`: For additional
          documentation.

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

    .. testcleanup:: downloading-experiment-data

        os.chdir(pwd)

    .. seealso::

        * :meth:`.nomad_nmr.Client.login`: For additional documentation.
        * :meth:`.nomad_nmr.Client.auto_experiments`: For additional
          documentation.
        * :meth:`.nomad_nmr.AutoExperiments.download`: For additional
          documentation.
        * :class:`.AutoExperimentQuery`: For additional documentation.

    .. _additional-filtering:

    **Additional filtering**

    Sometimes the filtering allowed by :class:`.AutoExperimentQuery` is not
    enough. In this case, you can use the :attr:`.AutoExperiments.inner`
    attribute to filter the experiments yourself, and then download only
    the experiments you want:

    .. testsetup:: additional-filtering

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

    .. testcode:: additional-filtering

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
            )
        )
        experiments.inner = [
            experiment
            for experiment in experiments
            if "special-study" in experiment.title
        ]
        Path("experiments.zip").write_bytes(experiments.download())

    .. testcleanup:: additional-filtering

        os.chdir(pwd)

    .. seealso::

        * :meth:`.nomad_nmr.Client.login`: For additional documentation.
        * :meth:`.nomad_nmr.Client.auto_experiments`: For additional
          documentation.
        * :meth:`.nomad_nmr.AutoExperiments.download`: For additional
          documentation.
        * :class:`.AutoExperimentQuery`: For additional documentation.

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
