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
        peak_df = bruker.nmr_peaks_df_1d(experiments.download())
        peak_df = nomad_nmr.add_metadata(client, peak_df)

    ::

        ┌─────────────────────────────────┬──────────┬──────────────┬────────────────────────────────┬───┬──────────────┬──────────┬──────────────────────────┬─────────────┐
        │ spectrum                        ┆ ppm      ┆ integral     ┆ auto_experiment_id             ┆ … ┆ submitted_at ┆ username ┆ group_id_right           ┆ group_name  │
        │ ---                             ┆ ---      ┆ ---          ┆ ---                            ┆   ┆ ---          ┆ ---      ┆ ---                      ┆ ---         │
        │ str                             ┆ f64      ┆ f64          ┆ str                            ┆   ┆ null         ┆ str      ┆ str                      ┆ str         │
        ╞═════════════════════════════════╪══════════╪══════════════╪════════════════════════════════╪═══╪══════════════╪══════════╪══════════════════════════╪═════════════╡
        │ 2410081201-0-1-lukasturcani/10… ┆ 8.344768 ┆ 20680.796875 ┆ 2410081201-0-1-lukasturcani-10 ┆ … ┆ null         ┆ test3    ┆ 672fdae0eb3b1c3c17062fee ┆ test-admins │
        │ 2410081201-0-1-lukasturcani/10… ┆ 8.339878 ┆ 31792.195312 ┆ 2410081201-0-1-lukasturcani-10 ┆ … ┆ null         ┆ test3    ┆ 672fdae0eb3b1c3c17062fee ┆ test-admins │
        │ 2410081201-0-1-lukasturcani/10… ┆ 8.338044 ┆ 20503.757812 ┆ 2410081201-0-1-lukasturcani-10 ┆ … ┆ null         ┆ test3    ┆ 672fdae0eb3b1c3c17062fee ┆ test-admins │
        │ 2410081201-0-1-lukasturcani/10… ┆ 8.336821 ┆ 10042.96875  ┆ 2410081201-0-1-lukasturcani-10 ┆ … ┆ null         ┆ test3    ┆ 672fdae0eb3b1c3c17062fee ┆ test-admins │
        │ 2410081201-0-1-lukasturcani/10… ┆ 8.323985 ┆ 10558.703125 ┆ 2410081201-0-1-lukasturcani-10 ┆ … ┆ null         ┆ test3    ┆ 672fdae0eb3b1c3c17062fee ┆ test-admins │
        │ …                               ┆ …        ┆ …            ┆ …                              ┆ … ┆ …            ┆ …        ┆ …                        ┆ …           │
        │ 2410161546-0-1-admin/10/pdata/… ┆ 1.398485 ┆ 10062.0      ┆ 2410161546-0-1-admin-10        ┆ … ┆ null         ┆ test1    ┆ 672fdae0eb3b1c3c17062fed ┆ group-1     │
        │ 2410161546-0-1-admin/10/pdata/… ┆ 1.238337 ┆ 4.8948e7     ┆ 2410161546-0-1-admin-10        ┆ … ┆ null         ┆ test1    ┆ 672fdae0eb3b1c3c17062fed ┆ group-1     │
        │ 2410161546-0-1-admin/10/pdata/… ┆ 1.051905 ┆ 31991.0      ┆ 2410161546-0-1-admin-10        ┆ … ┆ null         ┆ test1    ┆ 672fdae0eb3b1c3c17062fed ┆ group-1     │
        │ 2410161546-0-1-admin/10/pdata/… ┆ 1.048848 ┆ 41602.6875   ┆ 2410161546-0-1-admin-10        ┆ … ┆ null         ┆ test1    ┆ 672fdae0eb3b1c3c17062fed ┆ group-1     │
        │ 2410161546-0-1-admin/10/pdata/… ┆ 0.858137 ┆ 146085.9375  ┆ 2410161546-0-1-admin-10        ┆ … ┆ null         ┆ test1    ┆ 672fdae0eb3b1c3c17062fed ┆ group-1     │
        └─────────────────────────────────┴──────────┴──────────────┴────────────────────────────────┴───┴──────────────┴──────────┴──────────────────────────┴─────────────┘

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

    **Downloading auto experiment data**

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


    .. _viewing-experiment-data:

    **Gettting auto experiment data as a data frame**

    This example shows you have to get all the data held by
    :class:`.AutoExperiments` as a data frame, note that this does not
    download the spectrum data itself:

    .. testsetup:: viewing-experiment-data

        from aitomic import nomad_nmr
        import os

        client = nomad_nmr.Client.login(
            os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
            username="admin",
            password="foo",
        )

    .. testcode:: viewing-experiment-data

        experiments = client.auto_experiments()
        df = experiments.to_df()

    ::

        ┌──────────────────────────┬───────────────────────┬───────────────────┬─────────────────┬────────────┬────────────┬──────────────────────────┬──────────────────────────┬──────────────────────────┬─────────┬─────────────────────────┐
        │ auto_experiment_id       ┆ dataset_name          ┆ experiment_number ┆ parameter_set   ┆ parameters ┆ title      ┆ instrument_id            ┆ user_id                  ┆ group_id                 ┆ solvent ┆ submitted_at            │
        │ ---                      ┆ ---                   ┆ ---               ┆ ---             ┆ ---        ┆ ---        ┆ ---                      ┆ ---                      ┆ ---                      ┆ ---     ┆ ---                     │
        │ str                      ┆ str                   ┆ str               ┆ str             ┆ null       ┆ str        ┆ str                      ┆ str                      ┆ str                      ┆ str     ┆ datetime[μs, UTC]       │
        ╞══════════════════════════╪═══════════════════════╪═══════════════════╪═════════════════╪════════════╪════════════╪══════════════════════════╪══════════════════════════╪══════════════════════════╪═════════╪═════════════════════════╡
        │ 2106231050-2-1-test1-10  ┆ 2106231050-2-1-test1  ┆ 10                ┆ parameter-set-1 ┆ null       ┆ Test Exp 1 ┆ 672658eff9f290068dc027bd ┆ 672658eff9f290068dc027c5 ┆ 672658eff9f290068dc027c3 ┆ CDCl3   ┆ null                    │
        │ 2106231050-2-1-test1-11  ┆ 2106231050-2-1-test1  ┆ 11                ┆ parameter-set-1 ┆ null       ┆ Test Exp 1 ┆ 672658eff9f290068dc027bd ┆ 672658eff9f290068dc027c5 ┆ 672658eff9f290068dc027c3 ┆ CDCl3   ┆ null                    │
        │ 2106231055-3-2-test2-10  ┆ 2106231055-3-2-test2  ┆ 10                ┆ parameter-set-2 ┆ null       ┆ Test Exp 3 ┆ 672658eff9f290068dc027be ┆ 672658eff9f290068dc027c6 ┆ 672658eff9f290068dc027c3 ┆ C6D6    ┆ null                    │
        │ 2106231100-10-2-test3-10 ┆ 2106231100-10-2-test3 ┆ 10                ┆ parameter-set-3 ┆ null       ┆ Test Exp 4 ┆ 672658eff9f290068dc027bf ┆ 672658eff9f290068dc027c7 ┆ 672658eff9f290068dc027c3 ┆ C6D6    ┆ null                    │
        │ 2106240012-10-2-test2-10 ┆ 2106240012-10-2-test2 ┆ 10                ┆ parameter-set-3 ┆ null       ┆ Test Exp 5 ┆ 672658eff9f290068dc027bf ┆ 672658eff9f290068dc027c7 ┆ 672658eff9f290068dc027c3 ┆ C6D6    ┆ null                    │
        │ 2106241100-10-2-test3-10 ┆ 2106241100-10-2-test3 ┆ 10                ┆ parameter-set-3 ┆ null       ┆ Test Exp 6 ┆ 672658eff9f290068dc027bf ┆ 672658eff9f290068dc027c7 ┆ 672658eff9f290068dc027c4 ┆ CDCl3   ┆ null                    │
        │ 2106241100-10-2-test4-1  ┆ 2106241100-10-2-test4 ┆ 1                 ┆ parameter-set-3 ┆ null       ┆ Test Exp 7 ┆ 672658eff9f290068dc027bf ┆ 672658eff9f290068dc027c7 ┆ 672658eff9f290068dc027c4 ┆ CDCl3   ┆ 2024-01-01 00:00:00 UTC │
        └──────────────────────────┴───────────────────────┴───────────────────┴─────────────────┴────────────┴────────────┴──────────────────────────┴──────────────────────────┴──────────────────────────┴─────────┴─────────────────────────┘

    .. seealso::

        * :meth:`.nomad_nmr.Client.auto_experiments`: For additional
          documentation.
        * :meth:`.nomad_nmr.AutoExperiments.to_df`: For additional
          documentation.

    .. _joining-data-frames:

    **Joining data frames**

    Sometimes you may have two different data frames but want to join their data.
    For example, if you use :meth:`.nomad_nmr.AutoExperiments.to_df` you will have a
    data frame with all the user ids. However, you will probably want to filter data
    not by the user id but by the username. First lets create a data frame of auto
    experiments:

    .. testsetup:: joining-data-frames

        from aitomic import nomad_nmr
        import os
        import polars as pl

        client = nomad_nmr.Client.login(
            os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
            username="admin",
            password="foo",
        )

    .. testcode:: joining-data-frames

        experiments = client.auto_experiments().to_df()

    Then lets create a data frame of user data:

    .. testcode:: joining-data-frames

        users = client.users().to_df()

    and join the two data frames:

    .. testcode:: joining-data-frames

        experiments = experiments.join(users, on="user_id")

    Now we can filter the data frame by the username:

    .. testcode:: joining-data-frames

        experiments.filter(pl.col("username") == "fred")

    ::

        ┌──────────────────────────┬───────────────────────┬───────────────────┬─────────────────┬────────────┬────────────┬──────────────────────────┬──────────────────────────┬──────────────────────────┬─────────┬─────────────────────────┐
        │ auto_experiment_id       ┆ dataset_name          ┆ experiment_number ┆ parameter_set   ┆ parameters ┆ title      ┆ username                 ┆ user_id                  ┆ group_id                 ┆ solvent ┆ submitted_at            │
        │ ---                      ┆ ---                   ┆ ---               ┆ ---             ┆ ---        ┆ ---        ┆ ---                      ┆ ---                      ┆ ---                      ┆ ---     ┆ ---                     │
        │ str                      ┆ str                   ┆ str               ┆ str             ┆ null       ┆ str        ┆ str                      ┆ str                      ┆ str                      ┆ str     ┆ datetime[μs, UTC]       │
        ╞══════════════════════════╪═══════════════════════╪═══════════════════╪═════════════════╪════════════╪════════════╪══════════════════════════╪══════════════════════════╪══════════════════════════╪═════════╪═════════════════════════╡
        │ 2106231050-2-1-test1-10  ┆ 2106231050-2-1-test1  ┆ 10                ┆ parameter-set-1 ┆ null       ┆ Test Exp 1 ┆ fred                     ┆ 672658eff9f290068dc027c5 ┆ 672658eff9f290068dc027c3 ┆ CDCl3   ┆ null                    │
        │ 2106231050-2-1-test1-11  ┆ 2106231050-2-1-test1  ┆ 11                ┆ parameter-set-1 ┆ null       ┆ Test Exp 1 ┆ fred                     ┆ 672658eff9f290068dc027c5 ┆ 672658eff9f290068dc027c3 ┆ CDCl3   ┆ null                    │
        └──────────────────────────┴───────────────────────┴───────────────────┴─────────────────┴────────────┴────────────┴──────────────────────────┴──────────────────────────┴──────────────────────────┴─────────┴─────────────────────────┘


    In addition to users, you can also do this process with groups!

    .. seealso::

        * :meth:`.nomad_nmr.Client.auto_experiments`: For additional
          documentation.
        * :meth:`.nomad_nmr.Client.users`: For additional documentation.
        * :meth:`.nomad_nmr.Client.groups`: For additional documentation.

    .. _downloading-experiment-data-query:

    **Downloading auto experiment data matching a query**

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

"""  # noqa: E501

from aitomic._internal.nomad_nmr import (
    AuthToken,
    AutoExperiment,
    AutoExperimentQuery,
    AutoExperiments,
    Client,
    Group,
    Groups,
    User,
    Users,
    add_metadata,
)

__all__ = [
    "AuthToken",
    "AutoExperiment",
    "AutoExperimentQuery",
    "AutoExperiments",
    "Client",
    "Group",
    "Groups",
    "User",
    "Users",
    "add_metadata",
]
