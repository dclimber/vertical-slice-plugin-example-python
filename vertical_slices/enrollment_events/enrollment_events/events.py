from __future__ import annotations

from courses_events.events import CourseID
from eventsourcing.dcb.msgpack import Decision
from student_events.events import StudentID

__all__ = [
    "StudentJoinedCourse",
    "StudentLeftCourse",
]


class StudentJoinedCourse(Decision):
    student_id: StudentID
    course_id: CourseID


class StudentLeftCourse(Decision):
    student_id: StudentID
    course_id: CourseID
