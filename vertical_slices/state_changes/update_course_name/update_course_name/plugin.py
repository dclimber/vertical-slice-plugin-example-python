from __future__ import annotations

from typing import Protocol

from update_course_name.slice import UpdateCourseName


class UpdateCourseNameRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class UpdateCourseNamePlugin:
    name = "state-change.update-course-name"

    def register(self, registry: UpdateCourseNameRegistry) -> None:
        registry.command("course.update_name", UpdateCourseName)


update_course_name_plugin = UpdateCourseNamePlugin()
