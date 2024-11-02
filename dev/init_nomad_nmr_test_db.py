"""Populate a test NOMAD NMR database with data."""

import argparse
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, NewType

from bson.objectid import ObjectId
import pymongo
from pydantic import BaseModel, ConfigDict, Field
from pymongo.database import Database


def main() -> None:
    """Run the example."""
    args = _parse_args()

    client = pymongo.MongoClient[Any](args.uri)
    db = client.get_database("nomad")
    instruments = _add_instruments(db)
    parameter_sets = _add_parameter_sets(db, instruments)
    groups = _add_groups(db)
    users = _add_users(db, groups)
    _add_experiments(
        db=db,
        instruments=instruments,
        groups=groups,
        users=users,
        parameter_sets=parameter_sets,
        datastore=args.datastore,
    )


InstrumentId = NewType("InstrumentId", str)


class Instrument(BaseModel):
    """An instrument."""

    name: str
    is_active: bool = Field(alias="isActive")
    available: bool
    capacity: int
    day_allowance: int = Field(alias="dayAllowance")
    night_allowance: int = Field(alias="nightAllowance")
    overhead_time: int = Field(alias="overheadTime")
    cost: float


def _add_instruments(db: Database[Any]) -> list[InstrumentId]:
    collection = db.get_collection("instruments")
    collection.delete_many({})
    return [
        InstrumentId(str(id_))
        for id_ in collection.insert_many(
            [
                Instrument(
                    name="instrument-1",
                    isActive=True,
                    available=True,
                    capacity=60,
                    cost=3,
                    dayAllowance=2,
                    nightAllowance=105,
                    overheadTime=255,
                ).model_dump(),
                Instrument(
                    name="instrument-2",
                    isActive=False,
                    available=False,
                    capacity=60,
                    cost=2,
                    dayAllowance=20,
                    nightAllowance=195,
                    overheadTime=255,
                ).model_dump(),
                Instrument(
                    name="instrument-3",
                    isActive=True,
                    available=True,
                    capacity=24,
                    cost=2,
                    dayAllowance=20,
                    nightAllowance=195,
                    overheadTime=255,
                ).model_dump(),
            ]
        ).inserted_ids
    ]


class ParameterSet(BaseModel):
    """A parameter set."""

    name: str
    available_on: list[InstrumentId] = Field(alias="availableOn")


def _add_parameter_sets(
    db: Database[Any],
    instruments: list[InstrumentId],
) -> list[str]:
    collection = db.get_collection("parameterSets")
    collection.delete_many({})
    parameter_sets = [
        ParameterSet(
            name="parameter-set-1",
            availableOn=[instruments[0]],
        ),
        ParameterSet(
            name="parameter-set-2",
            availableOn=[instruments[1]],
        ),
        ParameterSet(
            name="parameter-set-3",
            availableOn=[instruments[0], instruments[2]],
        ),
    ]
    collection.insert_many(
        parameter_set.model_dump() for parameter_set in parameter_sets
    )
    return [parameter_set.name for parameter_set in parameter_sets]


GroupId = NewType("GroupId", str)


class Group(BaseModel):
    """A group."""

    name: str
    is_active: bool = Field(alias="isActive")
    description: str
    is_batch: bool = Field(alias="isBatch")
    data_access: str = Field(alias="dataAccess")


def _add_groups(db: Database[Any]) -> list[GroupId]:
    collection = db.get_collection("groups")
    collection.delete_many({"groupName": {"$ne": "default"}})
    return [
        GroupId(str(id_))
        for id_ in collection.insert_many(
            [
                Group(
                    name="group-1",
                    isActive=True,
                    description="Test group 1",
                    isBatch=False,
                    dataAccess="user",
                ).model_dump(),
                Group(
                    name="test-admins",
                    isActive=True,
                    description="Admins test group",
                    isBatch=True,
                    dataAccess="user",
                ).model_dump(),
            ]
        ).inserted_ids
    ]


UserId = NewType("UserId", str)


class User(BaseModel):
    """A user."""

    username: str
    full_name: str = Field(alias="fullName")
    email: str
    password: str
    is_active: bool = Field(alias="isActive")
    group: GroupId
    access_level: str = Field(alias="accessLevel")


def _add_users(db: Database[Any], groups: list[GroupId]) -> list[UserId]:
    collection = db.get_collection("users")
    collection.delete_many({})
    return [
        UserId(str(id_))
        for id_ in collection.insert_many(
            [
                User(
                    username="test1",
                    fullName="Test User 1",
                    email="test1@test.com",
                    password="t1p1",  # noqa: S106
                    isActive=False,
                    group=groups[0],
                    accessLevel="user",
                ).model_dump(),
                User(
                    username="test2",
                    fullName="Test User 2",
                    email="test2@test.com",
                    password="t2p2",  # noqa: S106
                    isActive=True,
                    group=groups[0],
                    accessLevel="user",
                ).model_dump(),
                User(
                    username="test3",
                    fullName="Test User 3",
                    email="test3@test.com",
                    password="t3p3",  # noqa: S106
                    isActive=True,
                    group=groups[1],
                    accessLevel="admin",
                ).model_dump(),
            ]
        ).inserted_ids
    ]


ExperimentId = NewType("ExperimentId", str)


class InstrumentInfo(BaseModel):
    """Information about an instrument."""

    id: InstrumentId
    name: str


class UserInfo(BaseModel):
    """Information about a user."""

    id: UserId
    username: str


class GroupInfo(BaseModel):
    """Information about a group."""

    id: GroupId
    name: str


class Experiment(BaseModel):
    """An experiment."""

    exp_id: str = Field(alias="expId")
    instrument: InstrumentInfo
    user: UserInfo
    group: GroupInfo
    dataset_name: str = Field(alias="datasetName")
    status: str
    title: str
    parameter_set: str = Field(alias="parameterSet")
    exp_no: str = Field(alias="expNo")
    holder: str
    data_path: Path = Field(alias="dataPath")
    solvent: str
    submitte_at: datetime | None = Field(default=None, alias="submittedAt")


def _add_experiments(  # noqa: PLR0913
    *,
    db: Database[Any],
    instruments: list[InstrumentId],
    groups: list[GroupId],
    users: list[UserId],
    parameter_sets: list[str],
    datastore: Path,
) -> list[ExperimentId]:
    collection = db.get_collection("experiments")
    collection.delete_many({})
    experiments = [
        Experiment(
            expId="2106231050-2-1-test1-10",
            instrument=InstrumentInfo(id=instruments[0], name="instrument-1"),
            user=UserInfo(id=users[0], username="test1"),
            group=GroupInfo(id=groups[0], name="group-1"),
            datasetName="2106231050-2-1-test1",
            status="Archived",
            title="Test Exp 1",
            parameterSet=parameter_sets[0],
            expNo="10",
            holder="2",
            dataPath=datastore / "2106231050-2-1-test1-10",
            solvent="CDCl3",
            submittedAt=None,
        ),
        Experiment(
            expId="2106231050-2-1-test1-11",
            instrument=InstrumentInfo(id=instruments[0], name="instrument-1"),
            user=UserInfo(id=users[0], username="test1"),
            group=GroupInfo(id=groups[0], name="group-1"),
            datasetName="2106231050-2-1-test1",
            status="Archived",
            title="Test Exp 1",
            parameterSet=parameter_sets[0],
            expNo="11",
            holder="2",
            dataPath=datastore / "2106231050-2-1-test1-11",
            solvent="CDCl3",
            submittedAt=None,
        ),
        Experiment(
            expId="2106231055-3-2-test2-10",
            instrument=InstrumentInfo(id=instruments[1], name="instrument-2"),
            user=UserInfo(id=users[1], username="test2"),
            group=GroupInfo(id=groups[0], name="group-1"),
            datasetName="2106231055-3-2-test2",
            status="Archived",
            title="Test Exp 3",
            parameterSet=parameter_sets[1],
            expNo="10",
            holder="3",
            dataPath=datastore / "2106231055-3-2-test2-10",
            solvent="C6D6",
            submittedAt=None,
        ),
        Experiment(
            expId="2106231100-10-2-test3-10",
            instrument=InstrumentInfo(id=instruments[2], name="instrument-2"),
            user=UserInfo(id=users[2], username="test3"),
            group=GroupInfo(id=groups[0], name="group-1"),
            datasetName="2106231100-10-2-test3",
            status="Archived",
            title="Test Exp 4",
            parameterSet=parameter_sets[2],
            expNo="10",
            holder="10",
            dataPath=datastore / "2106231100-10-2-test3-10",
            solvent="C6D6",
            submittedAt=None,
        ),
        Experiment(
            expId="2106240012-10-2-test2-10",
            instrument=InstrumentInfo(id=instruments[2], name="instrument-3"),
            user=UserInfo(id=users[2], username="test3"),
            group=GroupInfo(id=groups[0], name="group-1"),
            datasetName="2106240012-10-2-test2",
            status="Available",
            title="Test Exp 5",
            parameterSet=parameter_sets[2],
            expNo="10",
            holder="10",
            dataPath=datastore / "2106240012-10-2-test2-10",
            solvent="C6D6",
            submittedAt=None,
        ),
        Experiment(
            expId="2106241100-10-2-test3-10",
            instrument=InstrumentInfo(id=instruments[2], name="instrument-3"),
            user=UserInfo(id=users[2], username="test3"),
            group=GroupInfo(id=groups[1], name="group-2"),
            datasetName="2106241100-10-2-test3",
            status="Archived",
            title="Test Exp 6",
            parameterSet=parameter_sets[3],
            expNo="10",
            holder="10",
            dataPath=datastore / "2106241100-10-2-test3-10",
            solvent="CDCl3",
            submittedAt=None,
        ),
        Experiment(
            expId="2106241100-10-2-test4-1",
            instrument=InstrumentInfo(id=instruments[2], name="instrument-3"),
            user=UserInfo(id=users[2], username="test3"),
            group=GroupInfo(id=groups[1], name="group-2"),
            datasetName="2106241100-10-2-test4",
            status="Archived",
            title="Test Exp 7",
            parameterSet=parameter_sets[3],
            expNo="1",
            holder="11",
            dataPath=datastore / "2106241100-10-2-test4-1",
            solvent="CDCl3",
            submittedAt=datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC),
        ),
    ]
    ids = [
        ExperimentId(str(id_))
        for id_ in collection.insert_many(
            experiment.model_dump() for experiment in experiments
        ).inserted_ids
    ]
    for experiment in experiments:
        with (
            zipfile.ZipFile(
                datastore.joinpath(f"{experiment.exp_id}.zip"), "w"
            ) as archive,
            archive.open(f"{experiment.exp_id}.json", "w") as f,
        ):
            f.write(experiment.model_dump_json().encode())
    return ids


def _parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Populate a test NOMAD NMR database with data."
    )
    parser.add_argument(
        "uri",
        help="The URI of the NOMAD server.",
    )
    parser.add_argument(
        "datastore",
        help="The path to the NOMAD datastore.",
        type=Path,
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
