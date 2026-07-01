from __future__ import annotations

from course_kernel import Registry
from update_student_max_courses.slice import UpdateMaxCourses


class UpdateStudentMaxCoursesPlugin:
    name = "state-change.update-student-max-courses"

    def register(self, registry: Registry) -> None:
        registry.command("student.update_max_courses", UpdateMaxCourses)


update_student_max_courses_plugin = UpdateStudentMaxCoursesPlugin()
