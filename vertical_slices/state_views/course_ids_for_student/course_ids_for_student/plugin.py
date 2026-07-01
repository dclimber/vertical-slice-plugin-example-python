from __future__ import annotations

from course_kernel import Registry
from course_ids_for_student.view import CourseIDsForStudent


class CourseIDsForStudentPlugin:
    name = "state-view.course-ids-for-student"

    def register(self, registry: Registry) -> None:
        registry.query("enrollment.course_ids_for_student", CourseIDsForStudent)
        registry.query("enrolment.course_ids_for_student", CourseIDsForStudent)


course_ids_for_student_plugin = CourseIDsForStudentPlugin()
