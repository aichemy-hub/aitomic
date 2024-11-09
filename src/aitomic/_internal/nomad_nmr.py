from collections.abc import Iterator
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta

import polars as pl
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
    experiment_number: str = Field(alias="expNo")
    parameter_set: str = Field(alias="parameterSet")
    parameters: str | None = None
    title: str
    instrument: str
    user: str
    group: str
    solvent: str
    submitted_at: datetime | None = Field(default=None, alias="submittedAt")

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
            solvent=self.solvent,
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
        solvent: The id of the solvent used in the experiment.
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
    solvent: str
    """The id of the solvent used in the experiment."""
    submitted_at: datetime | None
    """The time the experiment was submitted."""


@dataclass(slots=True)
class AutoExperiments:
    """A collection of auto experiments.

    Examples:
        * :ref:`Getting an NMR peak data frame <getting-peak-df>`
        * :ref:`Downloading auto experiment data <downloading-experiment-data>`
        * :ref:`Getting auto experiment data as a data frame \
            <viewing-experiment-data>`

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
            * :ref:`Getting an NMR peak data frame <getting-peak-df>`
            * :ref:`Downloading experiment data <downloading-experiment-data>`

        Returns:
            The zip file as a series of bytes.

        Raises:
            requests.HTTPError: If the download request fails.
        """
        response = requests.post(
            f"{self.client.url}/api/v2/auto-experiments/download",
            params={"id": ",".join(experiment.id for experiment in self)},
            headers={
                "Authorization": f"Bearer {self.client.auth_token.token}"
            },
            timeout=self.client.timeout,
        )
        response.raise_for_status()
        return response.content

    def __iter__(self) -> Iterator[AutoExperiment]:
        """Iterate over the experiments."""
        return iter(self.inner)

    def __len__(self) -> int:
        """Get the number of experiments."""
        return len(self.inner)

    def to_df(self) -> pl.DataFrame:
        """Convert the experiment data into a data frame.

        Examples:
            * :ref:`Getting auto experiment data as a data frame \
              <viewing-experiment-data>`

        """
        return pl.DataFrame(
            {
                "auto_experiment_id": [
                    experiment.id for experiment in self.inner
                ],
                "dataset_name": [
                    experiment.dataset_name for experiment in self.inner
                ],
                "experiment_number": [
                    experiment.experiment_number for experiment in self.inner
                ],
                "parameter_set": [
                    experiment.parameter_set for experiment in self.inner
                ],
                "parameters": [
                    experiment.parameters for experiment in self.inner
                ],
                "title": [experiment.title for experiment in self.inner],
                "instrument_id": [
                    experiment.instrument for experiment in self.inner
                ],
                "user_id": [experiment.user for experiment in self.inner],
                "group_id": [experiment.group for experiment in self.inner],
                "solvent": [experiment.solvent for experiment in self.inner],
                "submitted_at": [
                    experiment.submitted_at for experiment in self.inner
                ],
            }
        )


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

    will match any experiment with a solvent of either ``DMSO`` or ``CDCl3``
    AND an experiment with a title of either ``test`` or ``test-1``.


    Examples:
        * :ref:`Downloading experiment data matching a query \
            <downloading-experiment-data-query>`

    Parameters:
        solvent: Filter for experiments with any of these solvents.
        instrument_id: Filter for experiments done on any of these instruments.
        parameter_set:
            Filter for experiments using any of these parameter sets.
        title: Filter for experiments with any of these titles.
        start_date: Filter for experiments submitted after this date.
        end_date: Filter for experiments submitted before this date.
        group_id: Filter for experiments belonging to any of these groups.
        user_id: Filter for experiments created by any of these users.
        dataset_name: Filter for experiments in any of these datasets.
        offset: Skip the first ``offset`` experiments.
        limit: Limit the number of experiments returned to ``limit``.

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


def to_query(query: AutoExperimentQuery) -> Iterator[tuple[str, str]]:
    for key, value in asdict(query).items():
        if value is not None:
            if isinstance(value, list):
                yield key, ",".join(value)
            else:
                yield key, value


@dataclass(slots=True, kw_only=True)
class User:
    """Data about a NOMAD user.

    Parameters:
        id: The user id.
        username: The username.
        group: The group the user belongs to.

    """

    id: str
    """The user id."""
    username: str
    """The username."""
    group: str
    """The id of the group the user belongs to."""


@dataclass(slots=True)
class Users:
    """A collection of users.

    Examples:
        * :ref:`Joining data frames <joining-data-frames>`

    Parameters:
        inner: The users.

    """

    inner: list[User]
    """The users."""

    def to_df(self) -> pl.DataFrame:
        """Convert the users into a data frame.

        Examples:
            * :ref:`Joining data frames <joining-data-frames>`

        """
        return pl.DataFrame(
            {
                "user_id": [user.id for user in self.inner],
                "username": [user.username for user in self.inner],
                "group_id": [user.group for user in self.inner],
            }
        )


@dataclass(slots=True, kw_only=True)
class Group:
    """Data about a NOMAD group.

    Parameters:
        id: The group id.
        name: The name of the group.

    """

    id: str
    """The group id."""
    name: str
    """The name of the group."""


@dataclass(slots=True)
class Groups:
    """A collection of groups.

    Examples:
        * :ref:`Joining data frames <joining-data-frames>`

    Parameters:
        inner: The groups.

    """

    inner: list[Group]
    """The groups."""

    def to_df(self) -> pl.DataFrame:
        """Convert the groups into a data frame.

        Examples:
            * :ref:`Joining data frames <joining-data-frames>`

        """
        return pl.DataFrame(
            {
                "group_id": [group.id for group in self.inner],
                "group_name": [group.name for group in self.inner],
            }
        )


@dataclass(slots=True)
class Client:
    """Client for interacting with a NOMAD server.

    Use the methods on the client send requests to the NOMAD server.

    Examples:
        * :ref:`Getting an NMR peak data frame <getting-peak-df>`
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

        Parameters:
            url: The URL of the NOMAD server.
            username: The username to use for authentication.
            password: The password to use for authentication.
            timeout: The timeout for requests.

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
            f"{self.url}/api/auth/login",
            json={
                "username": self.username,
                "password": self.password,
            },
            timeout=self.timeout,
        )
        response_.raise_for_status()
        response = AuthResponse.model_validate(response_.json())
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
            * :ref:`Getting an NMR peak data frame <getting-peak-df>`
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
            f"{self.url}/api/v2/auto-experiments",
            params={} if query is None else dict(to_query(query)),
            headers={"Authorization": f"Bearer {self.auth_token.token}"},
            timeout=self.timeout,
        )
        response.raise_for_status()

        return AutoExperiments(
            client=self,
            inner=[
                AutoExperimentResponse.model_validate(
                    experiment
                ).to_auto_experiment()
                for experiment in response.json()
            ],
        )

    def users(self) -> Users:
        """Get the users on the server.

        Examples:
            * :ref:`Joining data frames <joining-data-frames>`

        """
        response = requests.get(
            f"{self.url}/api/admin/users",
            headers={"Authorization": f"Bearer {self.auth_token.token}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return Users(
            inner=[
                User(
                    id=user["_id"],
                    username=user["username"],
                    group=user["group"]["_id"],
                )
                for user in response.json()["users"]
            ]
        )

    def groups(self) -> Groups:
        """Get the groups on the server.

        Examples:
            * :ref:`Joining data frames <joining-data-frames>`

        """
        response = requests.get(
            f"{self.url}/api/admin/groups",
            headers={"Authorization": f"Bearer {self.auth_token.token}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return Groups(
            inner=[
                Group(
                    id=group["_id"],
                    name=group["groupName"],
                )
                for group in response.json()
            ]
        )


def add_metadata(client: Client, spectra: pl.DataFrame) -> pl.DataFrame:
    auto_experiments = client.auto_experiments().to_df()
    users = client.users().to_df()
    groups = client.groups().to_df()
    spectra = spectra.with_columns(
        auto_experiment_id=(
            pl.col("spectrum")
            .str.extract(r"([^/]+/[^/]+)")
            .str.replace("/", "-")
        ),
    )
    return (
        spectra.join(auto_experiments, on="auto_experiment_id", how="left")
        .join(users, on="user_id", how="left")
        .join(groups, on="group_id", how="left")
    )
