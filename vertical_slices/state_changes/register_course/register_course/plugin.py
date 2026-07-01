from __future__ import annotations

from course_kernel import Registry
from register_course.slice import RegisterCourse


class RegisterCoursePlugin:
    name = "state-change.register-course"

    def register(self, registry: Registry) -> None:
        registry.command("course.register", RegisterCourse)


register_course_plugin = RegisterCoursePlugin()
