from __future__ import annotations

from pathlib import Path

import pytest

from register_student.plugin import register_student_plugin

from course_app.app import CourseApp
from course_app.main import create_app

ROOT = Path(__file__).resolve().parents[2]


def test_handle_command_raises_key_error_for_unregistered_command() -> None:
    app = CourseApp()

    with pytest.raises(KeyError, match="missing.command"):
        app.handle_command("missing.command")


def test_handle_query_raises_key_error_for_unregistered_query() -> None:
    app = CourseApp()

    with pytest.raises(KeyError, match="missing.query"):
        app.handle_query("missing.query")


def test_handle_command_executes_registered_student_register_slice() -> None:
    app = CourseApp()
    register_student_plugin.register(app.composition.registry)

    recorded = app.handle_command(
        "student.register",
        name="Max",
        max_courses=4,
    )

    assert recorded.student_id.startswith("student-")


def test_course_app_exposes_enrolment_workflow_methods() -> None:
    app = create_app(
        env={
            "PERSISTENCE_MODULE": "eventsourcing.dcb.popo",
        }
    )

    student_id = app.register_student(name="Alice", max_courses=1)
    course_id = app.register_course(name="Maths", places=1)

    app.join_course(student_id=student_id, course_id=course_id)

    assert app.list_students_for_course(course_id) == ["Alice"]
    assert app.list_courses_for_student(student_id) == ["Maths"]


def test_old_example_modules_are_not_part_of_the_public_repo() -> None:
    assert not (ROOT / "src/examples").exists()
    assert not (ROOT / "dcb_enrolment_with_vertical_slices").exists()
