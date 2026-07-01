from __future__ import annotations

import importlib
from dataclasses import dataclass, field


@dataclass
class RecordingRegistry:
    queries: dict[str, type] = field(default_factory=dict)

    def query(self, name: str, slice_factory: type) -> None:
        self.queries[name] = slice_factory


def test_state_view_plugins_register_canonical_query_names() -> None:
    registry = RecordingRegistry()

    plugin_modules = [
        "student_ids_for_course.plugin",
        "student_names.plugin",
        "course_ids_for_student.plugin",
        "course_names.plugin",
        "student_summary.plugin",
        "course_summary.plugin",
    ]
    plugin_names = [
        "student_ids_for_course_plugin",
        "student_names_plugin",
        "course_ids_for_student_plugin",
        "course_names_plugin",
        "student_summary_plugin",
        "course_summary_plugin",
    ]

    for module_name, plugin_name in zip(plugin_modules, plugin_names, strict=True):
        plugin = getattr(importlib.import_module(module_name), plugin_name)
        plugin.register(registry)

    assert registry.queries == {
        "enrollment.student_ids_for_course": importlib.import_module(
            "student_ids_for_course.view"
        ).StudentIDsForCourse,
        "enrolment.student_ids_for_course": importlib.import_module(
            "student_ids_for_course.view"
        ).StudentIDsForCourse,
        "enrollment.student_names": importlib.import_module(
            "student_names.view"
        ).StudentNames,
        "enrolment.student_names": importlib.import_module(
            "student_names.view"
        ).StudentNames,
        "enrollment.course_ids_for_student": importlib.import_module(
            "course_ids_for_student.view"
        ).CourseIDsForStudent,
        "enrolment.course_ids_for_student": importlib.import_module(
            "course_ids_for_student.view"
        ).CourseIDsForStudent,
        "enrollment.course_names": importlib.import_module(
            "course_names.view"
        ).CourseNames,
        "enrolment.course_names": importlib.import_module(
            "course_names.view"
        ).CourseNames,
        "enrollment.student": importlib.import_module("student_summary.view").Student,
        "enrolment.student": importlib.import_module("student_summary.view").Student,
        "enrollment.course": importlib.import_module("course_summary.view").Course,
        "enrolment.course": importlib.import_module("course_summary.view").Course,
    }
