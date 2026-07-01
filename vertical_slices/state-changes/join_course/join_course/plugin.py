from __future__ import annotations

from typing import Protocol

from join_course.slice import StudentJoinsCourse


class JoinCourseRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class JoinCoursePlugin:
    name = "state-change.join-course"

    def register(self, registry: JoinCourseRegistry) -> None:
        registry.command("enrollment.join_course", StudentJoinsCourse)
        registry.command("enrolment.join_course", StudentJoinsCourse)


join_course_plugin = JoinCoursePlugin()
