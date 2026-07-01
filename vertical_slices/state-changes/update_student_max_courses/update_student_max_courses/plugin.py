from __future__ import annotations

from typing import Protocol

from update_student_max_courses.slice import UpdateMaxCourses


class UpdateStudentMaxCoursesRegistry(Protocol):
    def command(self, name: str, slice_factory: type) -> None: ...


class UpdateStudentMaxCoursesPlugin:
    name = "state-change.update-student-max-courses"

    def register(self, registry: UpdateStudentMaxCoursesRegistry) -> None:
        registry.command("student.update_max_courses", UpdateMaxCourses)


update_student_max_courses_plugin = UpdateStudentMaxCoursesPlugin()
