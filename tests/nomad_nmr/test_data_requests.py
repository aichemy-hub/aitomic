import os

import polars as pl

from aitomic import nomad_nmr


def test_user_data_requests() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    users = (
        client.users()
        .to_df()
        .join(client.groups().to_df(), on="group_id")
        .drop("user_id", "group_id")
        .sort("username")
    )
    expected = pl.DataFrame(
        {
            "username": [
                "admin",
                "test1",
                "test2",
                "test3",
            ],
            "group_name": [
                "default",
                "group-1",
                "group-1",
                "test-admins",
            ],
        }
    ).sort("username")
    assert users.equals(expected)
