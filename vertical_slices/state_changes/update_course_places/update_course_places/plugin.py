from __future__ import annotations

from typing import Protocol

from update_course_places.slice import UpdateCoursePlaces


class UpdateCoursePlacesRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class UpdateCoursePlacesPlugin:
    name = "state-change.update-course-places"

    def register(self, registry: UpdateCoursePlacesRegistry) -> None:
        registry.command("course.update_places", UpdateCoursePlaces)


update_course_places_plugin = UpdateCoursePlacesPlugin()
