from __future__ import annotations

from courses_events.events import CourseID, CourseRegistered
from enrollment_events.errors import (
    CourseNotFoundError,
    NotAlreadyJoinedError,
    StudentNotFoundError,
)
from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import StudentID, StudentRegistered


class StudentLeavesCourse(Slice[StudentLeftCourse]):
    def __init__(self, student_id: StudentID, course_id: CourseID) -> None:
        self.student_id = student_id
        self.course_id = course_id
        self.course_was_registered = False
        self.student_was_registered = False
        self.students_on_course: list[StudentID] = []
        self.courses_for_student: list[CourseID] = []

    def consistency_boundary(self) -> list[Selector]:
        return [
            Selector(
                types=[StudentRegistered, StudentJoinedCourse, StudentLeftCourse],
                tags=[self.student_id],
            ),
            Selector(
                types=[CourseRegistered, StudentJoinedCourse, StudentLeftCourse],
                tags=[self.course_id],
            ),
        ]

    @event(StudentRegistered)
    def _(self) -> None:
        self.student_was_registered = True

    @event(CourseRegistered)
    def _(self) -> None:
        self.course_was_registered = True

    @event(StudentJoinedCourse)
    def _(self, student_id: StudentID, course_id: CourseID) -> None:
        if student_id == self.student_id:
            self.courses_for_student.append(course_id)
        if course_id == self.course_id:
            self.students_on_course.append(student_id)

    @event(StudentLeftCourse)
    def _(self, student_id: StudentID, course_id: CourseID) -> None:
        if student_id == self.student_id:
            self.courses_for_student.remove(course_id)
        if course_id == self.course_id:
            self.students_on_course.remove(student_id)

    def execute(self) -> None:
        if not self.course_was_registered:
            raise CourseNotFoundError
        if not self.student_was_registered:
            raise StudentNotFoundError
        if self.student_id not in self.students_on_course:
            raise NotAlreadyJoinedError
        self.trigger_event(
            StudentLeftCourse,
            tags=[self.student_id, self.course_id],
            student_id=self.student_id,
            course_id=self.course_id,
        )
