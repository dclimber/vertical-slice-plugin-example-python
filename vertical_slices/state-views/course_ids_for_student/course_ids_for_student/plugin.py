from __future__ import annotations

from typing import Protocol

from course_ids_for_student.view import CourseIDsForStudent


class CourseIDsForStudentRegistry(Protocol):
    def query(self, name: str, slice_factory: type) -> None: ...


class CourseIDsForStudentPlugin:
    name = "state-view.course-ids-for-student"

    def register(self, registry: CourseIDsForStudentRegistry) -> None:
        registry.query("enrollment.course_ids_for_student", CourseIDsForStudent)
        registry.query("enrolment.course_ids_for_student", CourseIDsForStudent)


course_ids_for_student_plugin = CourseIDsForStudentPlugin()
