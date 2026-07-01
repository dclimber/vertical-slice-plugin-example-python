from __future__ import annotations

from courses_events.events import CourseID
from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import StudentID


class StudentIDsForCourse(Slice[StudentJoinedCourse]):
    def __init__(self, course_id: CourseID) -> None:
        self.course_id = course_id
        self.student_ids: list[StudentID] = []

    def consistency_boundary(self) -> Selector:
        return Selector(types=type(self).projected_types, tags=[self.course_id])

    @event(StudentJoinedCourse)
    def _(self, student_id: StudentID) -> None:
        self.student_ids.append(student_id)

    @event(StudentLeftCourse)
    def _(self, student_id: StudentID) -> None:
        self.student_ids.remove(student_id)
