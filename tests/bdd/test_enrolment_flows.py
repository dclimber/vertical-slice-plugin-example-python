from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../../docs/features/enrolment/student_joins_course.feature",
    "Student joins a course with available capacity",
)
def test_student_joins_course() -> None:
    pass
