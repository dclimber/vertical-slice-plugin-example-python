from __future__ import annotations

from course_kernel import Registry
from update_course_places.slice import UpdateCoursePlaces


class UpdateCoursePlacesPlugin:
    name = "state-change.update-course-places"

    def register(self, registry: Registry) -> None:
        registry.command("course.update_places", UpdateCoursePlaces)


update_course_places_plugin = UpdateCoursePlacesPlugin()
