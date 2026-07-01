from __future__ import annotations

from typing import Protocol

from student_ids_for_course.view import StudentIDsForCourse


class StudentIDsForCourseRegistry(Protocol):
    def query(self, name: str, slice_factory: type) -> None: ...


class StudentIDsForCoursePlugin:
    name = "state-view.student-ids-for-course"

    def register(self, registry: StudentIDsForCourseRegistry) -> None:
        registry.query("enrollment.student_ids_for_course", StudentIDsForCourse)
        registry.query("enrolment.student_ids_for_course", StudentIDsForCourse)


student_ids_for_course_plugin = StudentIDsForCoursePlugin()
