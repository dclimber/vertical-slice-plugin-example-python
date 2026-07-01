from __future__ import annotations

from dataclasses import dataclass, field

from eventsourcing.dcb.domain import Selector
from examples.dcb_enrolment.interface import StudentID
from student_slice.events import (
    StudentMaxCoursesUpdated,
    StudentNameUpdated,
    StudentRegistered,
)
from student_slice.plugin import student_slice
from student_slice.slices import UpdateMaxCourses, UpdateStudentName

@dataclass
class RecordingRegistry:
    events: dict[str, type] = field(default_factory=dict)
    event_versions: dict[str, int] = field(default_factory=dict)

    def event(self, name: str, event_type: type, version: int) -> None:
        self.events[name] = event_type
        self.event_versions[name] = version


def test_student_slice_plugin_registers_events() -> None:
    registry = RecordingRegistry()

    student_slice.register(registry)

    assert registry.events == {
        "student.registered": StudentRegistered,
        "student.name_updated": StudentNameUpdated,
        "student.max_courses_updated": StudentMaxCoursesUpdated,
    }
    assert registry.event_versions == {
        "student.registered": 1,
        "student.name_updated": 1,
        "student.max_courses_updated": 1,
    }


def test_update_max_courses_watches_capacity_events_by_student_id() -> None:
    student_id = StudentID("student-123")

    selector = UpdateMaxCourses(student_id, max_courses=7).consistency_boundary()

    assert selector == Selector(
        types=[StudentRegistered, StudentMaxCoursesUpdated],
        tags=[student_id],
    )
    assert StudentNameUpdated not in selector.types


def test_update_student_name_does_not_conflict_with_update_max_courses() -> None:
    student_id = StudentID("student-123")

    rename_selector = UpdateStudentName(student_id, name="Mandy").consistency_boundary()
    capacity_selector = UpdateMaxCourses(student_id, max_courses=7).consistency_boundary()

    assert rename_selector == Selector(
        types=[StudentRegistered, StudentNameUpdated],
        tags=[student_id],
    )
    assert capacity_selector == Selector(
        types=[StudentRegistered, StudentMaxCoursesUpdated],
        tags=[student_id],
    )
    assert StudentMaxCoursesUpdated not in rename_selector.types
    assert StudentNameUpdated not in capacity_selector.types
