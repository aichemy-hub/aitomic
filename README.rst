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

For more documentation make sure to check out our `docs
<https://aitomic.readthedocs.io/en/stable/>`_. There's lots of examples and
it's easy to get started.

Installation
------------

You can install ``aitomic`` via pip:

.. code-block:: bash

    $ pip install aitomic
