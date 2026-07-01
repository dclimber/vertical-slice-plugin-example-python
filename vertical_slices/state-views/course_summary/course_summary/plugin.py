from __future__ import annotations

from typing import Protocol

from course_summary.view import Course


class CourseSummaryRegistry(Protocol):
    def query(self, name: str, slice_factory: type) -> None: ...


class CourseSummaryPlugin:
    name = "state-view.course-summary"

    def register(self, registry: CourseSummaryRegistry) -> None:
        registry.query("enrollment.course", Course)
        registry.query("enrolment.course", Course)


course_summary_plugin = CourseSummaryPlugin()
