from __future__ import annotations

from typing import Protocol

from student_names.view import StudentNames


class StudentNamesRegistry(Protocol):
    def query(self, name: str, slice_factory: type) -> None: ...


class StudentNamesPlugin:
    name = "state-view.student-names"

    def register(self, registry: StudentNamesRegistry) -> None:
        registry.query("enrollment.student_names", StudentNames)
        registry.query("enrolment.student_names", StudentNames)


student_names_plugin = StudentNamesPlugin()
