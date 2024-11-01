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

    .. testcode::

        from aitomic import nomad_nmr

        client = nomad_nmr.Client.login(
            "http://demo.nomad-nmr.uk",
            username="demo",
            password="dem0User",
        )
        experiments = client.auto_experiments()
        with open("experiments.zip", "wb") as f:
            f.write(experiments.download())

"""

from aitomic._internal.nomad_nmr import AuthToken, Client

__all__ = ["AuthToken", "Client"]
