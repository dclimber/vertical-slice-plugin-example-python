from __future__ import annotations

from course_kernel import Registry
from join_course.slice import StudentJoinsCourse


class JoinCoursePlugin:
    name = "state-change.join-course"

    def register(self, registry: Registry) -> None:
        registry.command("enrollment.join_course", StudentJoinsCourse)
        registry.command("enrolment.join_course", StudentJoinsCourse)


join_course_plugin = JoinCoursePlugin()
