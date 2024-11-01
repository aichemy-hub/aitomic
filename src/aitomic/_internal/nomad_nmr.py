from dataclasses import dataclass
from datetime import UTC, datetime

import requests


@dataclass(slots=True)
class AuthToken:
    """Authentication token for the NOMAD server.

    A token must be used to authenticate requests to the NOMAD server.
    Generally the token is produced internally by the :class:`Client`
    via the :meth:`Client.login` and :meth:`Client.auth`.

    Examples:

        .. _refreshing-the-token:

        **Refreshing the token**

        .. testsetup:: refreshing-the-token

            import os
            from aitomic import nomad_nmr

            client = nomad_nmr.Client.login(
                os.environ.get("NOMAD_NMR_URL", "http://localhost:8080"),
                username="admin",
                password="foo",
            )

        .. testcode:: refreshing-the-token

            if client.auth_token.expired():
                client.auth()

    Parameters:
        expires_at: The time when the token expires.
        token: The token itself.

    """

    expires_at: datetime
    """The time at which the token expires."""
    token: str
    """The token value."""

    def expired(self) -> bool:
        """Check if the token is expired."""
        return self.expires_at < datetime.now(UTC)


@dataclass(slots=True)
class Client:
    """Client for interacting with a NOMAD server.

    Use the methods on the client send requests to the NOMAD server.

    Examples:
        * :ref:`Downloading experiment data <downloading-experiment-data>`

    Parameters:
        url: The URL of the NOMAD server.
        username: The username to use for authentication.
        password: The password to use for authentication.
        auth_token: The authentication token to use for requests.

    """

    url: str
    """The URL of the NOMAD server."""
    username: str
    """The username to use for authentication."""
    password: str
    """The password to use for authentication."""
    auth_token: AuthToken
    """The authentication token to use for requests."""

    @staticmethod
    def login(url: str, *, username: str, password: str) -> "Client":
        """Create a new client by logging into the NOMAD server.

        Examples:
            * :ref:`Downloading experiment data <downloading-experiment-data>`

        Raises:
            requests.HTTPError: If the login request fails.

        """
        response = requests.post(
            f"{url}/api/auth/login",
            data={"username": username, "password": password},
            timeout=5,
        )
        response.raise_for_status()

    def auth(self) -> None:
        """Make the client use a new authentication token.

        Examples:
            * :ref:`Refreshing the token <refreshing-the-token>`

        Raises:
            requests.HTTPError: If the authentication request fails.

        """
