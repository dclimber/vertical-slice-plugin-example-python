from __future__ import annotations

from course_kernel import Registry
from student_ids_for_course.view import StudentIDsForCourse


class StudentIDsForCoursePlugin:
    name = "state-view.student-ids-for-course"

    def register(self, registry: Registry) -> None:
        registry.query("enrollment.student_ids_for_course", StudentIDsForCourse)
        registry.query("enrolment.student_ids_for_course", StudentIDsForCourse)


student_ids_for_course_plugin = StudentIDsForCoursePlugin()
