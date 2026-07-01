from __future__ import annotations

import pytest

from course_app.main import create_app

pytest_plugins = [
    "tests.bdd.steps.command_steps",
    "tests.bdd.steps.query_steps",
]


@pytest.fixture
def app():
    return create_app(
        env={
            "PERSISTENCE_MODULE": "eventsourcing.dcb.popo",
        }
    )


@pytest.fixture
def bdd_context() -> dict[str, object]:
    return {
        "last_result": None,
        "vars": {},
    }
