from __future__ import annotations

from typing import Protocol

from courses_events.events import CourseNameUpdated, CoursePlacesUpdated, CourseRegistered


class CourseRegistry(Protocol):
    def event(self, name: str, event_type: type, version: int) -> None: ...


class CourseSlicePlugin:
    name: str = "course"

    def register(self, registry: CourseRegistry) -> None:
        registry.event("course.registered", CourseRegistered, version=1)
        registry.event("course.name_updated", CourseNameUpdated, version=1)
        registry.event("course.places_updated", CoursePlacesUpdated, version=1)


course_slice = CourseSlicePlugin()
