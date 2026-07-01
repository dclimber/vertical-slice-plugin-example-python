from __future__ import annotations

import ast
from pathlib import Path

from course_app.app import CourseApp
from course_app.main import create_app
from course_app.use_cases import register_use_cases

ROOT = Path(__file__).resolve().parents[2]
USE_CASES_MODULE = ROOT / "src/course_app/use_cases.py"


def test_register_use_cases_registers_all_expected_commands_and_queries() -> None:
    app = CourseApp()

    register_use_cases(app)

    assert set(app.composition.registry.commands) == {
        "student.register",
        "student.update_name",
        "student.update_max_courses",
        "course.register",
        "course.update_name",
        "course.update_places",
        "enrollment.join_course",
        "enrollment.leave_course",
        "enrolment.join_course",
        "enrolment.leave_course",
    }
    assert set(app.composition.registry.queries) == {
        "enrollment.student_ids_for_course",
        "enrollment.student_names",
        "enrollment.course_ids_for_student",
        "enrollment.course_names",
        "enrollment.student",
        "enrollment.course",
        "enrolment.student_ids_for_course",
        "enrolment.student_names",
        "enrolment.course_ids_for_student",
        "enrolment.course_names",
        "enrolment.student",
        "enrolment.course",
    }


def test_register_use_cases_defines_and_validates_expected_use_cases() -> None:
    app = CourseApp()

    register_use_cases(app)

    register_student = app.composition.use_cases["student.register"]
    assert register_student.slices == ["state-change.register-student"]
    assert register_student.commands == ["student.register"]

    register_course = app.composition.use_cases["course.register"]
    assert register_course.slices == ["state-change.register-course"]
    assert register_course.commands == ["course.register"]

    joins_course = app.composition.use_cases["enrolment.student_joins_course"]
    assert joins_course.slices == [
        "state-change.register-student",
        "state-change.register-course",
        "state-change.join-course",
        "state-view.student-ids-for-course",
        "state-view.student-names",
    ]
    assert joins_course.commands == [
        "student.register",
        "course.register",
        "enrollment.join_course",
    ]
    assert joins_course.queries == [
        "enrollment.student_ids_for_course",
        "enrollment.student_names",
    ]

    leaves_course = app.composition.use_cases["enrolment.student_leaves_course"]
    assert leaves_course.slices == [
        "state-change.leave-course",
        "state-view.course-summary",
        "state-view.student-summary",
    ]
    assert leaves_course.commands == ["enrollment.leave_course"]
    assert leaves_course.queries == ["enrollment.course", "enrollment.student"]


def test_create_app_returns_app_with_registered_and_validated_composition() -> None:
    app = create_app()

    assert isinstance(app, CourseApp)
    assert "student.register" in app.composition.registry.commands
    assert "enrollment.student" in app.composition.registry.queries


def test_register_use_cases_module_does_not_import_broad_domain_plugin_wrappers() -> None:
    module = ast.parse(USE_CASES_MODULE.read_text())

    imported_modules = {
        node.module
        for node in module.body
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }

    assert "student_slice.plugin" not in imported_modules
    assert "course_slice.plugin" not in imported_modules
    assert "enrolment_slice.plugin" not in imported_modules
