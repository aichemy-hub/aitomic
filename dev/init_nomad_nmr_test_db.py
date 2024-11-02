"""Populate a test NOMAD NMR database with data."""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any, NewType

import pymongo
from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from pymongo.database import Database


def main() -> None:
    """Run the example."""
    args = _parse_args()

    client = pymongo.MongoClient[Any](args.uri)
    db = client.get_database("nomad")
    instruments = _add_instruments(db)
    _add_parameter_sets(db, instruments)
    groups = _add_groups(db)
    users = _add_users(db, groups)
    _add_experiments(db, instruments, groups, users, args.datastore)


InstrumentId = NewType("InstrumentId", ObjectId)


class Instrument(BaseModel):
    """An instrument."""

    id: InstrumentId | None = None
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
    return collection.insert_many(
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
            ),
            Instrument(
                id=None,
                name="instrument-2",
                isActive=False,
                available=False,
                capacity=60,
                cost=2,
                dayAllowance=20,
                nightAllowance=195,
                overheadTime=255,
            ),
            Instrument(
                id=None,
                name="instrument-3",
                isActive=True,
                available=True,
                capacity=24,
                cost=2,
                dayAllowance=20,
                nightAllowance=195,
                overheadTime=255,
            ),
        ]
    ).inserted_ids


ParameterSetId = NewType("ParameterSetId", ObjectId)


class ParameterSet(BaseModel):
    """A parameter set."""

    id: ParameterSetId | None = None
    name: str
    available_on: list[InstrumentId] = Field(alias="availableOn")


def _add_parameter_sets(
    db: Database[Any],
    instruments: list[InstrumentId],
) -> list[ParameterSetId]:
    collection = db.get_collection("parameter_sets")
    collection.delete_many({})
    return collection.insert_many(
        [
            ParameterSet(
                name="parameter-set-1",
                availableOn=[instruments[0]],
            ),
            ParameterSet(
                id=None,
                name="parameter-set-2",
                availableOn=[instruments[1]],
            ),
            ParameterSet(
                id=None,
                name="parameter-set-3",
                availableOn=[instruments[0], instruments[2]],
            ),
        ]
    ).inserted_ids


GroupId = NewType("GroupId", ObjectId)


class Group(BaseModel):
    """A group."""

    id: GroupId | None = None
    name: str
    is_active: bool = Field(alias="isActive")
    description: str
    is_batch: bool = Field(alias="isBatch")
    data_access: str = Field(alias="dataAccess")


def _add_groups(db: Database[Any]) -> list[GroupId]:
    collection = db.get_collection("groups")
    collection.delete_many({"groupName": {"$ne": "default"}})
    return collection.insert_many(
        [
            Group(
                name="group-1",
                isActive=True,
                description="Test group 1",
                isBatch=False,
                dataAccess="user",
            ),
            Group(
                id=None,
                name="test-admins",
                isActive=True,
                description="Admins test group",
                isBatch=True,
                dataAccess="user",
            ),
        ]
    ).inserted_ids


UserId = NewType("UserId", ObjectId)


class User(BaseModel):
    """A user."""

    id: UserId | None = None
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
    return collection.insert_many(
        [
            User(
                username="test1",
                fullName="Test User 1",
                email="test1@test.com",
                password="t1p1",  # noqa: S106
                isActive=False,
                group=groups[0],
                accessLevel="user",
            ),
            User(
                id=None,
                username="test2",
                fullName="Test User 2",
                email="test2@test.com",
                password="t2p2",  # noqa: S106
                isActive=True,
                group=groups[0],
                accessLevel="user",
            ),
            User(
                id=None,
                username="test3",
                fullName="Test User 3",
                email="test3@test.com",
                password="t3p3",  # noqa: S106
                isActive=True,
                group=groups[1],
                accessLevel="admin",
            ),
        ]
    ).inserted_ids


ExperimentId = NewType("ExperimentId", ObjectId)


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

    id: ExperimentId | None = None
    exp_id: str = Field(alias="expId")
    instrument: InstrumentInfo
    user: UserInfo
    group: GroupInfo
    dataset_name: str = Field(alias="datasetName")
    status: str
    title: str
    parameter_set: ParameterSetId
    exp_no: str = Field(alias="expNo")
    holder: str
    data_path: Path = Field(alias="dataPath")
    sovlent: str
    submitted_at: datetime | None = Field(default=None, alias="submittedAt")


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
