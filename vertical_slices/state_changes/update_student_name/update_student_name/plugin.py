from __future__ import annotations

from course_kernel import Registry
from update_student_name.slice import UpdateStudentName


class UpdateStudentNamePlugin:
    name = "state-change.update-student-name"

    def register(self, registry: Registry) -> None:
        registry.command("student.update_name", UpdateStudentName)


update_student_name_plugin = UpdateStudentNamePlugin()
