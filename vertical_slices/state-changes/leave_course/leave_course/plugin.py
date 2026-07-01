from __future__ import annotations

from typing import Protocol

from leave_course.slice import StudentLeavesCourse


class LeaveCourseRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class LeaveCoursePlugin:
    name = "state-change.leave-course"

    def register(self, registry: LeaveCourseRegistry) -> None:
        registry.command("enrollment.leave_course", StudentLeavesCourse)
        registry.command("enrolment.leave_course", StudentLeavesCourse)


leave_course_plugin = LeaveCoursePlugin()
