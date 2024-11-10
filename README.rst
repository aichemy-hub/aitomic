:Docs: https://aitomic.readthedocs.io/en/stable/

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
