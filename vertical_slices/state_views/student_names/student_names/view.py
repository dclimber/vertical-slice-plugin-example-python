from __future__ import annotations

from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from student_events.events import StudentID, StudentNameUpdated, StudentRegistered


class StudentNames(Slice[StudentRegistered]):
    def __init__(self, student_ids: list[StudentID]) -> None:
        self.student_id_names: dict[StudentID, str | None] = dict.fromkeys(
            student_ids, None
        )

    def consistency_boundary(self) -> list[Selector]:
        return [
            Selector(types=type(self).projected_types, tags=[student_id])
            for student_id in self.student_id_names
        ]

    @event(StudentRegistered)
    def _(self, student_id: StudentID, name: str) -> None:
        self.student_id_names[student_id] = name

    @event(StudentNameUpdated)
    def _(self, student_id: StudentID, name: str) -> None:
        self.student_id_names[student_id] = name

    @property
    def names(self) -> list[str]:
        return [name for name in self.student_id_names.values() if name]
