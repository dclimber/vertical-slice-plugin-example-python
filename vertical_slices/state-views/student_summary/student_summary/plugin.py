from __future__ import annotations

from typing import Protocol

from student_summary.view import Student


class StudentSummaryRegistry(Protocol):
    def query(self, name: str, slice_factory: type) -> None: ...


class StudentSummaryPlugin:
    name = "state-view.student-summary"

    def register(self, registry: StudentSummaryRegistry) -> None:
        registry.query("enrollment.student", Student)
        registry.query("enrolment.student", Student)


student_summary_plugin = StudentSummaryPlugin()
