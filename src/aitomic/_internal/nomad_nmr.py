from dataclasses import dataclass
from datetime import UTC, datetime


class RequestError(Exception):
    """Raised when a request to the NOMAD server fails."""


@dataclass(slots=True)
class AuthToken:
    """Authentication token for the NOMAD server.

    A token must be used to authenticate requests to the NOMAD server.
    Generally the token is produced internally by the :class:`Client`
    via the :meth:`Client.login` and :meth:`Client.auth`.

    Examples:

        .. _refreshing-the-token:

        **Refreshing the token**

        .. testcode::

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
    def login() -> "Client":
        """Create a new client by logging into the NOMAD server.

        Examples:
            * :ref:`Downloading experiment data <downloading-experiment-data>`

        Raises:
            RequestError: If the login request fails.

        """
        pass

    def auth(self) -> None:
        """Make the client use a new authentication token.

        Examples:
            * :ref:`Refreshing the token <refreshing-the-token>`

        Raises:
            RequestError: If the authentication request fails.

        """
        pass
