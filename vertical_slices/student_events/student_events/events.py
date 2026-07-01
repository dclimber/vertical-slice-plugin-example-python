from __future__ import annotations

from eventsourcing.dcb.msgpack import Decision
from examples.dcb_enrolment.interface import StudentID

__all__ = [
    "StudentID",
    "StudentRegistered",
    "StudentNameUpdated",
    "StudentMaxCoursesUpdated",
]


class StudentRegistered(Decision):
    student_id: StudentID
    name: str
    max_courses: int


class StudentNameUpdated(Decision):
    student_id: StudentID
    name: str


class StudentMaxCoursesUpdated(Decision):
    student_id: StudentID
    max_courses: int
