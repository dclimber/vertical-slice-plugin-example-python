from __future__ import annotations

from courses_events.events import CourseID
from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import StudentID


class CourseIDsForStudent(Slice[StudentJoinedCourse]):
    def __init__(self, student_id: StudentID) -> None:
        self.student_id = student_id
        self.course_ids: list[CourseID] = []

    def consistency_boundary(self) -> Selector:
        return Selector(types=type(self).projected_types, tags=[self.student_id])

    @event(StudentJoinedCourse)
    def _(self, course_id: CourseID) -> None:
        self.course_ids.append(course_id)

    @event(StudentLeftCourse)
    def _(self, course_id: CourseID) -> None:
        self.course_ids.remove(course_id)
