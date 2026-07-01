from __future__ import annotations

from uuid import uuid4

from eventsourcing.dcb.domain import Selector, Slice
from examples.dcb_enrolment.interface import StudentID
from student_events.events import StudentRegistered


class RegisterStudent(Slice[StudentRegistered]):
    def __init__(self, name: str, max_courses: int) -> None:
        self.student_id = StudentID(f"student-{uuid4()}")
        self.name = name
        self.max_courses = max_courses

    def consistency_boundary(self) -> Selector:
        return Selector(types=[StudentRegistered], tags=[self.student_id])

    def execute(self) -> None:
        self.trigger_event(
            StudentRegistered,
            tags=[self.student_id],
            student_id=self.student_id,
            name=self.name,
            max_courses=self.max_courses,
        )
