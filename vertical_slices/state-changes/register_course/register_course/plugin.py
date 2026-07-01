from __future__ import annotations

from typing import Protocol

from register_course.slice import RegisterCourse


class RegisterCourseRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class RegisterCoursePlugin:
    name = "state-change.register-course"

    def register(self, registry: RegisterCourseRegistry) -> None:
        registry.command("course.register", RegisterCourse)


register_course_plugin = RegisterCoursePlugin()
