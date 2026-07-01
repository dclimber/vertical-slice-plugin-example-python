from __future__ import annotations

from typing import Protocol

from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse


class EnrolmentRegistry(Protocol):
    def event(self, name: str, event_type: type, version: int) -> None: ...

    def consumes(self, event_name: str) -> None: ...


class EnrolmentSlicePlugin:
    name: str = "enrolment"

    def register(self, registry: EnrolmentRegistry) -> None:
        registry.event("enrolment.student_joined_course", StudentJoinedCourse, version=1)
        registry.event("enrolment.student_left_course", StudentLeftCourse, version=1)

        registry.consumes("student.registered")
        registry.consumes("student.name_updated")
        registry.consumes("student.max_courses_updated")
        registry.consumes("course.registered")
        registry.consumes("course.name_updated")
        registry.consumes("course.places_updated")


enrolment_slice = EnrolmentSlicePlugin()
