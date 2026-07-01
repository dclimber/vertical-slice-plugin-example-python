from __future__ import annotations

from typing import Protocol

from course_names.view import CourseNames


class CourseNamesRegistry(Protocol):
    def query(self, name: str, slice_factory: type) -> None: ...


class CourseNamesPlugin:
    name = "state-view.course-names"

    def register(self, registry: CourseNamesRegistry) -> None:
        registry.query("enrollment.course_names", CourseNames)
        registry.query("enrolment.course_names", CourseNames)


course_names_plugin = CourseNamesPlugin()
