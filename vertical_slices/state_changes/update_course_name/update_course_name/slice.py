from __future__ import annotations

from courses_events.events import CourseNameUpdated, CourseRegistered
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from courses_events.events import CourseID


class UpdateCourseName(Slice[CourseNameUpdated]):
    def __init__(self, course_id: CourseID, name: str) -> None:
        self.course_id = course_id
        self.name = name
        self.course_was_registered = False

    def consistency_boundary(self) -> Selector:
        return Selector(
            types=[CourseRegistered, CourseNameUpdated],
            tags=[self.course_id],
        )

    @event(CourseRegistered)
    def _(self) -> None:
        self.course_was_registered = True

    def execute(self) -> None:
        assert self.course_was_registered
        self.trigger_event(
            CourseNameUpdated,
            tags=[self.course_id],
            course_id=self.course_id,
            name=self.name,
        )
