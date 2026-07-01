from __future__ import annotations

from typing import Protocol

from student_events.events import (
    StudentMaxCoursesUpdated,
    StudentNameUpdated,
    StudentRegistered,
)


class StudentRegistry(Protocol):
    def event(self, name: str, event_type: type, version: int) -> None: ...


class StudentSlicePlugin:
    name: str = "student"

    def register(self, registry: StudentRegistry) -> None:
        registry.event("student.registered", StudentRegistered, version=1)
        registry.event("student.name_updated", StudentNameUpdated, version=1)
        registry.event("student.max_courses_updated", StudentMaxCoursesUpdated, version=1)


student_slice = StudentSlicePlugin()
