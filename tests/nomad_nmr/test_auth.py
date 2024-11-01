import os
from datetime import timedelta

from aitomic import nomad_nmr


def test_auth() -> None:
    client = nomad_nmr.Client.login(
        os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
        username="admin",
        password="foo",  # noqa: S106
    )
    assert not client.auth_token.expired()

    client.auth_token.expires_at = client.auth_token.expires_at - timedelta(
        days=1
    )
    assert client.auth_token.expired()
    client.auth()
    assert not client.auth_token.expired()
