from __future__ import annotations

from course_kernel import Registry
from student_summary.view import Student


class StudentSummaryPlugin:
    name = "state-view.student-summary"

    def register(self, registry: Registry) -> None:
        registry.query("enrollment.student", Student)
        registry.query("enrolment.student", Student)


student_summary_plugin = StudentSummaryPlugin()
