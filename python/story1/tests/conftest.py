from mixer.backend.sqlalchemy import Mixer
import pytest

from instapolyglot.database import (
    engine,
    ModelBase,
    session_builder,
)


@pytest.fixture
def db_engine():
    return engine


@pytest.fixture
def db_session():
    return session_builder()


@pytest.yield_fixture(autouse=True)
def clean_database(db_engine):
    ModelBase.metadata.create_all(db_engine)

    yield

    ModelBase.metadata.drop_all(db_engine)


@pytest.fixture
def mixer(db_session):
    return Mixer(session=db_session, commit=True)
