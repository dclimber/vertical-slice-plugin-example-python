from __future__ import annotations

from courses_events.events import CoursePlacesUpdated, CourseRegistered
from eventsourcing.dcb.domain import Selector, Slice
from eventsourcing.domain import event
from examples.dcb_enrolment.interface import CourseID


class UpdateCoursePlaces(Slice[CoursePlacesUpdated]):
    def __init__(self, course_id: CourseID, places: int) -> None:
        self.course_id = course_id
        self.places = places
        self.course_was_registered = False

    def consistency_boundary(self) -> Selector:
        return Selector(
            types=[CourseRegistered, CoursePlacesUpdated],
            tags=[self.course_id],
        )

    @event(CourseRegistered)
    def _(self) -> None:
        self.course_was_registered = True

    def execute(self) -> None:
        assert self.course_was_registered
        self.trigger_event(
            CoursePlacesUpdated,
            tags=[self.course_id],
            course_id=self.course_id,
            places=self.places,
        )


UpdatePlaces = UpdateCoursePlaces
