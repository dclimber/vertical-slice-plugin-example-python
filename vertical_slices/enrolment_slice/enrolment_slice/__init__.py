from __future__ import annotations

from enrolment_slice.events import StudentJoinedCourse, StudentLeftCourse
from enrolment_slice.plugin import EnrolmentSlicePlugin, enrolment_slice
from enrolment_slice.queries import (
    Course,
    CourseIDs,
    CourseIDsForStudent,
    CourseNames,
    Student,
    StudentIDsForCourse,
    StudentNames,
    StudentsIDs,
)
from enrolment_slice.slices import StudentJoinsCourse, StudentLeavesCourse

__all__ = [
    "Course",
    "CourseIDs",
    "CourseIDsForStudent",
    "CourseNames",
    "EnrolmentSlicePlugin",
    "Student",
    "StudentIDsForCourse",
    "StudentJoinedCourse",
    "StudentJoinsCourse",
    "StudentLeftCourse",
    "StudentLeavesCourse",
    "StudentNames",
    "StudentsIDs",
    "enrolment_slice",
]
