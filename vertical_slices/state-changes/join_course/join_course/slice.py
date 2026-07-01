from __future__ import annotations

from courses_events.events import CourseID, CoursePlacesUpdated, CourseRegistered
from enrollment_events.errors import (
    AlreadyJoinedError,
    CourseNotFoundError,
    FullyBookedError,
    StudentNotFoundError,
    TooManyCoursesError,
)
from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import StudentID, StudentMaxCoursesUpdated, StudentRegistered


class StudentJoinsCourse(Slice[StudentJoinedCourse]):
    def __init__(self, student_id: StudentID, course_id: CourseID) -> None:
        self.student_id = student_id
        self.course_id = course_id
        self.course_was_registered = False
        self.student_was_registered = False
        self.student_max_courses = 0
        self.course_places = 0
        self.students_on_course: list[StudentID] = []
        self.courses_for_student: list[CourseID] = []

    def consistency_boundary(self) -> list[Selector]:
        return [
            Selector(
                types=[
                    StudentRegistered,
                    StudentMaxCoursesUpdated,
                    StudentJoinedCourse,
                    StudentLeftCourse,
                ],
                tags=[self.student_id],
            ),
            Selector(
                types=[
                    CourseRegistered,
                    CoursePlacesUpdated,
                    StudentJoinedCourse,
                    StudentLeftCourse,
                ],
                tags=[self.course_id],
            ),
        ]

    @event(StudentRegistered)
    def _(self, max_courses: int) -> None:
        self.student_was_registered = True
        self.student_max_courses = max_courses

    @event(CourseRegistered)
    def _(self, places: int) -> None:
        self.course_was_registered = True
        self.course_places = places

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

    @event(StudentMaxCoursesUpdated)
    def _(self, max_courses: int) -> None:
        self.student_max_courses = max_courses

    @event(CoursePlacesUpdated)
    def _(self, places: int) -> None:
        self.course_places = places

    def execute(self) -> None:
        if not self.course_was_registered:
            raise CourseNotFoundError(self.course_id)
        if not self.student_was_registered:
            raise StudentNotFoundError(self.student_id)
        if len(self.students_on_course) >= self.course_places:
            raise FullyBookedError(self.course_id)
        if len(self.courses_for_student) >= self.student_max_courses:
            raise TooManyCoursesError(self.student_id)
        if self.student_id in self.students_on_course:
            raise AlreadyJoinedError((self.student_id, self.course_id))
        self.trigger_event(
            StudentJoinedCourse,
            tags=[self.student_id, self.course_id],
            student_id=self.student_id,
            course_id=self.course_id,
        )
