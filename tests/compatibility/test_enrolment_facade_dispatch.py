from __future__ import annotations

from types import SimpleNamespace

from dcb_enrolment_with_vertical_slices.application import EnrolmentWithVerticalSlices
from examples.dcb_enrolment.interface import CourseID, StudentID


class SpyEnrolmentWithVerticalSlices(EnrolmentWithVerticalSlices):
    def __init__(self) -> None:
        self.command_calls: list[tuple[str, dict[str, object]]] = []
        self.query_calls: list[tuple[str, dict[str, object]]] = []

    def handle_command(self, name: str, /, **kwargs: object) -> object:
        self.command_calls.append((name, kwargs))
        if name == "student.register":
            return SimpleNamespace(student_id=StudentID("student-123"))
        if name == "course.register":
            return SimpleNamespace(course_id=CourseID("course-456"))
        return SimpleNamespace()

    def handle_query(self, name: str, /, **kwargs: object) -> object:
        self.query_calls.append((name, kwargs))
        if name == "enrollment.student_ids_for_course":
            return SimpleNamespace(student_ids=[StudentID("student-123")])
        if name == "enrollment.student_names":
            return SimpleNamespace(names=["Max"])
        if name == "enrollment.course_ids_for_student":
            return SimpleNamespace(course_ids=[CourseID("course-456")])
        if name == "enrollment.course_names":
            return SimpleNamespace(names=["Maths"])
        return SimpleNamespace()


def test_register_student_delegates_to_handle_command_and_returns_student_id() -> None:
    app = SpyEnrolmentWithVerticalSlices()

    student_id = app.register_student(name="Max", max_courses=2)

    assert student_id == "student-123"
    assert app.command_calls == [
        ("student.register", {"name": "Max", "max_courses": 2}),
    ]


def test_list_students_for_course_composes_queries_and_returns_names() -> None:
    app = SpyEnrolmentWithVerticalSlices()

    names = app.list_students_for_course(CourseID("course-456"))

    assert names == ["Max"]
    assert app.query_calls == [
        ("enrollment.student_ids_for_course", {"course_id": "course-456"}),
        ("enrollment.student_names", {"student_ids": ["student-123"]}),
    ]


def test_list_courses_for_student_composes_queries_and_returns_names() -> None:
    app = SpyEnrolmentWithVerticalSlices()

    names = app.list_courses_for_student(StudentID("student-123"))

    assert names == ["Maths"]
    assert app.query_calls == [
        ("enrollment.course_ids_for_student", {"student_id": "student-123"}),
        ("enrollment.course_names", {"course_ids": ["course-456"]}),
    ]
