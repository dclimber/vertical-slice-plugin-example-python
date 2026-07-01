from __future__ import annotations

import importlib
from dataclasses import dataclass, field


@dataclass
class RecordingRegistry:
    commands: dict[str, type] = field(default_factory=dict)

    def command(self, name: str, slice_factory: type) -> None:
        self.commands[name] = slice_factory


def test_state_change_plugins_register_canonical_command_names() -> None:
    registry = RecordingRegistry()

    plugin_modules = [
        "register_student.plugin",
        "update_student_name.plugin",
        "update_student_max_courses.plugin",
        "register_course.plugin",
        "update_course_name.plugin",
        "update_course_places.plugin",
        "join_course.plugin",
        "leave_course.plugin",
    ]
    plugin_names = [
        "register_student_plugin",
        "update_student_name_plugin",
        "update_student_max_courses_plugin",
        "register_course_plugin",
        "update_course_name_plugin",
        "update_course_places_plugin",
        "join_course_plugin",
        "leave_course_plugin",
    ]

    for module_name, plugin_name in zip(plugin_modules, plugin_names, strict=True):
        plugin = getattr(importlib.import_module(module_name), plugin_name)
        plugin.register(registry)

    assert registry.commands == {
        "student.register": importlib.import_module("register_student.slice").RegisterStudent,
        "student.update_name": importlib.import_module(
            "update_student_name.slice"
        ).UpdateStudentName,
        "student.update_max_courses": importlib.import_module(
            "update_student_max_courses.slice"
        ).UpdateMaxCourses,
        "course.register": importlib.import_module("register_course.slice").RegisterCourse,
        "course.update_name": importlib.import_module(
            "update_course_name.slice"
        ).UpdateCourseName,
        "course.update_places": importlib.import_module(
            "update_course_places.slice"
        ).UpdateCoursePlaces,
        "enrollment.join_course": importlib.import_module(
            "join_course.slice"
        ).StudentJoinsCourse,
        "enrolment.join_course": importlib.import_module(
            "join_course.slice"
        ).StudentJoinsCourse,
        "enrollment.leave_course": importlib.import_module(
            "leave_course.slice"
        ).StudentLeavesCourse,
        "enrolment.leave_course": importlib.import_module(
            "leave_course.slice"
        ).StudentLeavesCourse,
    }
