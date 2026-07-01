from __future__ import annotations

from course_kernel import Registry
from student_names.view import StudentNames


class StudentNamesPlugin:
    name = "state-view.student-names"

    def register(self, registry: Registry) -> None:
        registry.query("enrollment.student_names", StudentNames)
        registry.query("enrolment.student_names", StudentNames)


student_names_plugin = StudentNamesPlugin()
