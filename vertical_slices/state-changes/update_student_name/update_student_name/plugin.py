from __future__ import annotations

from typing import Protocol

from update_student_name.slice import UpdateStudentName


class UpdateStudentNameRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class UpdateStudentNamePlugin:
    name = "state-change.update-student-name"

    def register(self, registry: UpdateStudentNameRegistry) -> None:
        registry.command("student.update_name", UpdateStudentName)


update_student_name_plugin = UpdateStudentNamePlugin()
