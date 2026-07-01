from __future__ import annotations

from typing import Protocol

from register_student.slice import RegisterStudent


class RegisterStudentRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class RegisterStudentPlugin:
    name = "state-change.register-student"

    def register(self, registry: RegisterStudentRegistry) -> None:
        registry.command("student.register", RegisterStudent)


register_student_plugin = RegisterStudentPlugin()
