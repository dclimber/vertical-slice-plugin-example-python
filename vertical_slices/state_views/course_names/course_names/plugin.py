from __future__ import annotations

from course_kernel import Registry
from course_names.view import CourseNames


class CourseNamesPlugin:
    name = "state-view.course-names"

    def register(self, registry: Registry) -> None:
        registry.query("enrollment.course_names", CourseNames)
        registry.query("enrolment.course_names", CourseNames)


course_names_plugin = CourseNamesPlugin()
