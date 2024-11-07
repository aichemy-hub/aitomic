import os

from aitomic import nomad_nmr


def test_users() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    users = client.users()
    assert users == [
        nomad_nmr.User(
            id="",
            username="test1",
            group="",
        ),
        nomad_nmr.User(
            id="6c0f7e0e-a2d7-4f9c-b9f0-f4b0a3f1f3e9",
            username="test1",
            group="test-admins",
        ),
    ]
