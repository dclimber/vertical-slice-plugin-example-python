from __future__ import annotations

from course_kernel import Registry
from leave_course.slice import StudentLeavesCourse


class LeaveCoursePlugin:
    name = "state-change.leave-course"

    def register(self, registry: Registry) -> None:
        registry.command("enrollment.leave_course", StudentLeavesCourse)
        registry.command("enrolment.leave_course", StudentLeavesCourse)


leave_course_plugin = LeaveCoursePlugin()
