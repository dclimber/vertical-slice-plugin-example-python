from __future__ import annotations

from course_kernel import Registry
from course_summary.view import Course


class CourseSummaryPlugin:
    name = "state-view.course-summary"

    def register(self, registry: Registry) -> None:
        registry.query("enrollment.course", Course)
        registry.query("enrolment.course", Course)


course_summary_plugin = CourseSummaryPlugin()
