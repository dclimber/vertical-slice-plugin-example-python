from __future__ import annotations

import pytest

from register_student.plugin import register_student_plugin

from course_app.app import CourseApp


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
