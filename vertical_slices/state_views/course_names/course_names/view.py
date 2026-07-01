from __future__ import annotations

from courses_events.events import CourseID, CourseNameUpdated, CourseRegistered
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event


class CourseNames(Slice[CourseRegistered]):
    def __init__(self, course_ids: list[CourseID]) -> None:
        self.course_id_names: dict[CourseID, str | None] = dict.fromkeys(
            course_ids, None
        )

    def consistency_boundary(self) -> list[Selector]:
        return [
            Selector(types=type(self).projected_types, tags=[course_id])
            for course_id in self.course_id_names
        ]

    @event(CourseRegistered)
    def _(self, course_id: CourseID, name: str) -> None:
        self.course_id_names[course_id] = name

    @event(CourseNameUpdated)
    def _(self, course_id: CourseID, name: str) -> None:
        self.course_id_names[course_id] = name

    @property
    def names(self) -> list[str]:
        return [name for name in self.course_id_names.values() if name]
