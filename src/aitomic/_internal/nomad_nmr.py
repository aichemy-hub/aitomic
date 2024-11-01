from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import requests
from pydantic import BaseModel, Field


class AuthResponse(BaseModel):
    expires_in: int = Field(alias="expiresIn")
    token: str


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


class AutoExperimentResponse(BaseModel):
    id: str
    dataset_name: str = Field(alias="datasetName")
    experiment_number: str = Field(alias="experimentNo")
    parameter_set: str = Field(alias="parameterSet")
    parameters: str | None
    title: str
    instrument: str
    user: str
    group: str
    sovlent: str
    submitted_at: datetime = Field(alias="submittedAt")

    def to_auto_experiment(self) -> "AutoExperiment":
        return AutoExperiment(
            id=self.id,
            dataset_name=self.dataset_name,
            experiment_number=self.experiment_number,
            parameter_set=self.parameter_set,
            parameters=self.parameters,
            title=self.title,
            instrument=self.instrument,
            user=self.user,
            group=self.group,
            sovlent=self.sovlent,
            submitted_at=self.submitted_at,
        )


@dataclass(slots=True, kw_only=True)
class AutoExperiment:
    """Data about an auto experiment stored in NOMAD.

    Parameters:
        id: The experiment ID.
        dataset_name: The name of the dataset the experiment belongs to.
        experiment_number: The experiment number.
        parameter_set: The parameter set used to run the experiment.
        parameters: The parameters used to run the experiment.
        title: The title of the experiment.
        instrument: The id of the instrument used to run the experiment.
        user: The id of the user who ran the experiment.
        group: The id of the group the experiment belongs to.
        sovlent: The id of the solvent used in the experiment.
        submitted_at: The time the experiment was submitted.
    """

    id: str
    """The experiment id."""
    dataset_name: str
    """The name of the dataset the experiment belongs to."""
    experiment_number: str
    """The experiment number."""
    parameter_set: str
    """The parameter set used to run the experiment."""
    parameters: str | None
    """The parameters used to run the experiment."""
    title: str
    """The title of the experiment."""
    instrument: str
    """The id of the instrument used to run the experiment."""
    user: str
    """The id of the user who ran the experiment."""
    group: str
    """The id of the group the experiment belongs to."""
    sovlent: str
    """The id of the solvent used in the experiment."""
    submitted_at: datetime
    """The time the experiment was submitted."""


@dataclass(slots=True)
class AutoExperiments:
    """A collection of auto experiments.

    Examples:
        * :ref:`Downloading experiment data <downloading-experiment-data>`

    Parameters:
        client: The client to use for requests.
        inner: The auto experiments.

    """

    client: "Client"
    """The client to use for requests."""
    inner: list[AutoExperiment]
    """The auto experiments."""

    def download(self) -> bytes:
        """Download the experiments into a zip file.

        Examples:
            * :ref:`Downloading experiment data <downloading-experiment-data>`

        Returns:
            The zip file as a series of bytes.

        Raises:
            requests.HTTPError: If the download request fails.
        """
        response = requests.post(
            f"{self.client.url}/api/v2/auto-experiments/download",
            params={"id": [experiment.id for experiment in self]},
            timeout=self.client.timeout,
        )
        response.raise_for_status()
        return response.content

    def __iter__(self) -> Iterator[AutoExperiment]:
        """Iterate over the experiments."""
        return iter(self.inner)


@dataclass(slots=True, kw_only=True)
class AutoExperimentQuery:
    """Query for auto experiments.

    Most of the parameters here can be either a single value or a list of
    values. If a list is provided, the query will match if any of the values
    match. For example, this query:

    .. testsetup::

        from aitomic import nomad_nmr

    .. testcode::

        query = nomad_nmr.AutoExperimentQuery(
            solvent=["DMSO", "CDCl3"],
            title=["test", "test-1"],
        )

    will match any experiment with a solvent of either DMSO or CDCl3 AND an
    experiment with a title of either test or test-1.


    Examples:
        * :ref:`Downloading experiment data matching a query \
            <downloading-experiment-data-query>`

    """

    solvent: str | list[str] | None = None
    """Filter for experiments with any of these solvents."""
    instrument_id: str | list[str] | None = None
    """Filter for experiments done on any of these instruments."""
    parameter_set: str | list[str] | None = None
    """Filter for experiments using any of these parameter sets."""
    title: str | list[str] | None = None
    """Filter for experiments with any of these titles."""
    start_date: datetime | None = None
    """Filter for experiments submitted after this date."""
    end_date: datetime | None = None
    """Filter for experiments submitted before this date."""
    group_id: str | list[str] | None = None
    """Filter for experiments belonging to any of these groups."""
    user_id: str | list[str] | None = None
    """Filter for experiments created by any of these users."""
    dataset_name: str | list[str] | None = None
    """Filter for experiments in any of these datasets."""
    offset: int | None = None
    """Skip the first ``offset`` experiments."""
    limit: int | None = None
    """Limit the number of experiments returned to ``limit``."""


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
        timeout: The timeout for requests.

    """

    url: str
    """The URL of the NOMAD server."""
    username: str
    """The username to use for authentication."""
    password: str
    """The password to use for authentication."""
    auth_token: AuthToken
    """The authentication token to use for requests."""
    timeout: float = 5.0
    """The timeout for requests."""

    @staticmethod
    def login(
        url: str, *, username: str, password: str, timeout: float = 5.0
    ) -> "Client":
        """Create a new client by logging into the NOMAD server.

        Examples:
            * :ref:`Downloading experiment data <downloading-experiment-data>`

        Raises:
            requests.HTTPError: If the login request fails.

        """
        response_ = requests.post(
            f"{url}/api/auth/login",
            json={
                "username": username,
                "password": password,
            },
            timeout=timeout,
        )
        response_.raise_for_status()
        response = AuthResponse.model_validate(response_.json())
        return Client(
            url=url,
            username=username,
            password=password,
            auth_token=AuthToken(
                expires_at=datetime.now(UTC)
                + timedelta(seconds=response.expires_in),
                token=response.token,
            ),
            timeout=timeout,
        )

    def auth(self) -> None:
        """Make the client use a new authentication token.

        Examples:
            * :ref:`Refreshing the token <refreshing-the-token>`

        Raises:
            requests.HTTPError: If the authentication request fails.

        """
        response_ = requests.post(
            f"{self.url}/api/v2/auth/token",
            json={
                "username": self.username,
                "password": self.password,
            },
            timeout=self.timeout,
        )
        response_.raise_for_status()
        response = AuthResponse.model_validate(response_)
        self.auth_token = AuthToken(
            expires_at=datetime.now(UTC)
            + timedelta(seconds=response.expires_in),
            token=response.token,
        )

    def auto_experiments(
        self, query: AutoExperimentQuery | None = None
    ) -> AutoExperiments:
        """Get a collection of auto experiments.

        Examples:
            * :ref:`Downloading experiment data <downloading-experiment-data>`
            * :ref:`Downloading experiment data matching a query \
                <downloading-experiment-data-query>`

        Parameters:
            query: The query to use for filtering the experiments.

        Returns:
            The collection of auto experiments.

        Raises:
            requests.HTTPError: If the request fails.
        """

        response = requests.get(
            f"{self.url}/api/v2/auto-experiments", params={}
        )
