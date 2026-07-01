from __future__ import annotations

from course_kernel import Registry
from update_course_name.slice import UpdateCourseName


class UpdateCourseNamePlugin:
    name = "state-change.update-course-name"

    def register(self, registry: Registry) -> None:
        registry.command("course.update_name", UpdateCourseName)


update_course_name_plugin = UpdateCourseNamePlugin()
