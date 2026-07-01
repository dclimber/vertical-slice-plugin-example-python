from __future__ import annotations

from uuid import uuid4

from courses_events.events import CourseRegistered
from eventsourcing.dcb.domain import Selector, Slice
from examples.dcb_enrolment.interface import CourseID


class RegisterCourse(Slice[CourseRegistered]):
    def __init__(self, name: str, places: int) -> None:
        self.name = name
        self.places = places
        self.course_id = CourseID(f"course-{uuid4()}")

    def consistency_boundary(self) -> Selector:
        return Selector(types=[CourseRegistered], tags=[self.course_id])

    def execute(self) -> None:
        self.trigger_event(
            CourseRegistered,
            tags=[self.course_id],
            course_id=self.course_id,
            name=self.name,
            places=self.places,
        )
