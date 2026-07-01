from __future__ import annotations

from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from examples.dcb_enrolment.interface import StudentID
from student_events.events import StudentMaxCoursesUpdated, StudentRegistered


class UpdateMaxCourses(Slice[StudentMaxCoursesUpdated]):
    def __init__(self, student_id: StudentID, max_courses: int) -> None:
        self.student_id = student_id
        self.max_courses = max_courses
        self.student_was_registered = False

    def consistency_boundary(self) -> Selector:
        return Selector(
            types=[StudentRegistered, StudentMaxCoursesUpdated],
            tags=[self.student_id],
        )

    @event(StudentRegistered)
    def _(self) -> None:
        self.student_was_registered = True

    def execute(self) -> None:
        assert self.student_was_registered
        self.trigger_event(
            StudentMaxCoursesUpdated,
            tags=[self.student_id],
            student_id=self.student_id,
            max_courses=self.max_courses,
        )
