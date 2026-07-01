from __future__ import annotations

from student_slice.events import (
    StudentMaxCoursesUpdated,
    StudentNameUpdated,
    StudentRegistered,
)
from student_slice.plugin import StudentSlicePlugin, student_slice
from student_slice.slices import RegisterStudent, UpdateMaxCourses, UpdateStudentName

__all__ = [
    "RegisterStudent",
    "StudentMaxCoursesUpdated",
    "StudentNameUpdated",
    "StudentRegistered",
    "StudentSlicePlugin",
    "UpdateMaxCourses",
    "UpdateStudentName",
    "student_slice",
]
