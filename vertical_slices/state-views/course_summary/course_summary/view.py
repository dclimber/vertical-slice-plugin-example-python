from __future__ import annotations

from courses_events.events import CourseID, CourseNameUpdated, CoursePlacesUpdated, CourseRegistered
from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import StudentID


class Course(Slice[CourseRegistered]):
    def __init__(self, course_id: CourseID) -> None:
        self.course_id = course_id
        self.course_was_registered = False
        self.name = ""
        self.places = 0
        self.student_ids: list[StudentID] = []

    def consistency_boundary(self) -> Selector:
        return Selector(tags=[self.course_id])

    @event(CourseRegistered)
    def _(self, name: str, places: int) -> None:
        self.course_was_registered = True
        self.name = name
        self.places = places

    @event(CourseNameUpdated)
    def _(self, name: str) -> None:
        self.name = name

    @event(CoursePlacesUpdated)
    def _(self, places: int) -> None:
        self.places = places

    @event(StudentJoinedCourse)
    def _(self, student_id: StudentID) -> None:
        self.student_ids.append(student_id)

    @event(StudentLeftCourse)
    def _(self, student_id: StudentID) -> None:
        self.student_ids.remove(student_id)
