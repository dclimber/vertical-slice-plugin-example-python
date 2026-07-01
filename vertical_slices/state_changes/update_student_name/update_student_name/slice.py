from __future__ import annotations

from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import StudentID
from student_events.events import StudentNameUpdated, StudentRegistered


class UpdateStudentName(Slice[StudentNameUpdated]):
    def __init__(self, student_id: StudentID, name: str) -> None:
        self.id = student_id
        self.name = name
        self.student_was_registered = False

    def consistency_boundary(self) -> Selector:
        return Selector(types=[StudentRegistered, StudentNameUpdated], tags=[self.id])

    @event(StudentRegistered)
    def _(self) -> None:
        self.student_was_registered = True

    def execute(self) -> None:
        assert self.student_was_registered
        self.trigger_event(
            StudentNameUpdated,
            tags=[self.id],
            student_id=self.id,
            name=self.name,
        )
