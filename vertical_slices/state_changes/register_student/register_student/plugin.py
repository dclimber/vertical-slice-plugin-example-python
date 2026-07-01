from __future__ import annotations

from course_kernel import Registry
from register_student.slice import RegisterStudent


class RegisterStudentPlugin:
    name = "state-change.register-student"

    def register(self, registry: Registry) -> None:
        registry.command("student.register", RegisterStudent)


register_student_plugin = RegisterStudentPlugin()
