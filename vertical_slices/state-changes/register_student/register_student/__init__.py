from __future__ import annotations

from register_student.plugin import RegisterStudentPlugin, register_student_plugin
from register_student.slice import RegisterStudent

__all__ = [
    "RegisterStudent",
    "RegisterStudentPlugin",
    "register_student_plugin",
]
