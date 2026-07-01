from __future__ import annotations

from courses_events.events import CourseID
from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import (
    StudentID,
    StudentMaxCoursesUpdated,
    StudentNameUpdated,
    StudentRegistered,
)


class Student(Slice[StudentRegistered]):
    def __init__(self, student_id: StudentID) -> None:
        self.student_id = student_id
        self.student_was_registered = False
        self.name = ""
        self.max_courses = 0
        self.course_ids: list[CourseID] = []

    def consistency_boundary(self) -> Selector:
        return Selector(tags=[self.student_id])

    @event(StudentRegistered)
    def _(self, name: str, max_courses: int) -> None:
        self.student_was_registered = True
        self.name = name
        self.max_courses = max_courses

    @event(StudentNameUpdated)
    def _(self, name: str) -> None:
        self.name = name

    @event(StudentMaxCoursesUpdated)
    def _(self, max_courses: int) -> None:
        self.max_courses = max_courses

    @event(StudentJoinedCourse)
    def _(self, course_id: CourseID) -> None:
        self.course_ids.append(course_id)

    @event(StudentLeftCourse)
    def _(self, course_id: CourseID) -> None:
        self.course_ids.remove(course_id)
