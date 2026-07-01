from __future__ import annotations

from dataclasses import dataclass, field

from course_slice.events import CourseNameUpdated, CoursePlacesUpdated, CourseRegistered
from courses_events.events import CourseID
from enrolment_slice.events import StudentJoinedCourse, StudentLeftCourse
from enrolment_slice.plugin import enrolment_slice
from enrolment_slice.slices import StudentJoinsCourse, StudentLeavesCourse
from student_events.events import StudentID
from student_slice.events import (
    StudentMaxCoursesUpdated,
    StudentNameUpdated,
    StudentRegistered,
)


@dataclass
class RecordingRegistry:
    events: dict[str, type] = field(default_factory=dict)
    event_versions: dict[str, int] = field(default_factory=dict)
    consumed_events: list[str] = field(default_factory=list)

    def event(self, name: str, event_type: type, version: int) -> None:
        self.events[name] = event_type
        self.event_versions[name] = version

    def consumes(self, event_name: str) -> None:
        self.consumed_events.append(event_name)


def test_enrolment_slice_plugin_registers_events_and_consumes() -> None:
    registry = RecordingRegistry()

    enrolment_slice.register(registry)

    assert registry.events == {
        "enrolment.student_joined_course": StudentJoinedCourse,
        "enrolment.student_left_course": StudentLeftCourse,
    }
    assert registry.event_versions == {
        "enrolment.student_joined_course": 1,
        "enrolment.student_left_course": 1,
    }
    assert registry.consumed_events == [
        "student.registered",
        "student.name_updated",
        "student.max_courses_updated",
        "course.registered",
        "course.name_updated",
        "course.places_updated",
    ]


def test_student_joins_course_watches_student_capacity_events_by_student_id() -> None:
    student_id = StudentID("student-123")
    course_id = CourseID("course-456")

    selectors = StudentJoinsCourse(student_id, course_id).consistency_boundary()

    assert selectors[0].types == [
        StudentRegistered,
        StudentMaxCoursesUpdated,
        StudentJoinedCourse,
        StudentLeftCourse,
    ]
    assert selectors[0].tags == [student_id]
    assert StudentNameUpdated not in selectors[0].types


def test_student_joins_course_watches_course_capacity_events_by_course_id() -> None:
    student_id = StudentID("student-123")
    course_id = CourseID("course-456")

    selectors = StudentJoinsCourse(student_id, course_id).consistency_boundary()

    assert selectors[1].types == [
        CourseRegistered,
        CoursePlacesUpdated,
        StudentJoinedCourse,
        StudentLeftCourse,
    ]
    assert selectors[1].tags == [course_id]
    assert CourseNameUpdated not in selectors[1].types


def test_student_leaves_course_does_not_watch_name_updates() -> None:
    student_id = StudentID("student-123")
    course_id = CourseID("course-456")

    selectors = StudentLeavesCourse(student_id, course_id).consistency_boundary()

    assert selectors[0].types == [
        StudentRegistered,
        StudentJoinedCourse,
        StudentLeftCourse,
    ]
    assert selectors[0].tags == [student_id]
    assert StudentNameUpdated not in selectors[0].types

    assert selectors[1].types == [
        CourseRegistered,
        StudentJoinedCourse,
        StudentLeftCourse,
    ]
    assert selectors[1].tags == [course_id]
    assert CourseNameUpdated not in selectors[1].types
