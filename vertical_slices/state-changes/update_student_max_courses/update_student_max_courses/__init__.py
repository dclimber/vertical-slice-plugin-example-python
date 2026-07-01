from __future__ import annotations

from update_student_max_courses.plugin import (
    UpdateStudentMaxCoursesPlugin,
    update_student_max_courses_plugin,
)
from update_student_max_courses.slice import UpdateMaxCourses

__all__ = [
    "UpdateMaxCourses",
    "UpdateStudentMaxCoursesPlugin",
    "update_student_max_courses_plugin",
]
