:Docs: https://aitomic.readthedocs.io/en/stable/
:EPSRC Grant: EP/Y028775/1

aitomic
=======

``aitomic`` is a Python library developed by the `AIchemy Hub
<https://aichemy.ac.uk>`_ for making AI in chemistry simple. As a chemical
researcher, you likely do not want to spend your time thinking about how to
organize your data or collect it from various sources. Most likely, you want to
write simple function call and get access to all your data in a data frame.
Well, thats what ``aitomic`` does for you. Currently, the library provides
tools for accessing your NMR data stored in a `NOMAD NMR
<https://www.nomad-nmr.uk>`_ server. For example:


.. code-block:: python

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

For more documentation make sure to check out our `docs
<https://aitomic.readthedocs.io/en/stable/>`_. There's lots of examples and
it's easy to get started.

Installation
------------

You can install ``aitomic`` via pip:

.. code-block:: bash

  $ pip install aitomic


Development Notes
-----------------

UV
~~~

This repository uses `uv <https://docs.astral.sh/uv/>`_ to manage the
development environment. You can install uv by running the following command:

.. code-block:: bash

  $ pip install uv

Once you have uv installed, you can set up the development environment by running
the following command:

.. code-block:: bash

  $ uv sync --all-extras --dev

From then on, you can run any command using uv with ``uv run``.

See the `uv documentation <https://docs.astral.sh/uv/>`_ for more information.

Git LFS
~~~~~~~

This repository uses Git LFS to store large files. If you are cloning the
repository, make sure to have Git LFS installed. You can find more information
about Git LFS in the `official documentation
<https://git-lfs.github.com>`_.

Unit Tests
~~~~~~~~~~

The unit tests are written using `pytest <https://docs.pytest.org/en/stable/>`_.
To run the tests, you must have a local NOMAD NMR server running. You can
install the server by following the instructions in the `NOMAD NMR
repository <https://github.com/nomad-nmr/nomad-server?tab=readme-ov-file#set-up-for-development>`_.

Once you have the server running, you must initialize the test database by
running the following command:

.. code-block:: bash

  $ uv run dev/init_nomad_nmr_test_db.py mongodb://localhost:27017 <PARENT_PATH>/nomad-server/datastore dev/nmr-data

Where ``<PARENT_PATH>`` is the path to the NOMAD NMR server repository.

You can then run the tests by running the following command:

.. code-block:: bash

  $ uv run pytest --cov=src --cov-report term-missing

Documentation
~~~~~~~~~~~~~

The documentation is built using `Sphinx <https://www.sphinx-doc.org/en/master/>`_.
