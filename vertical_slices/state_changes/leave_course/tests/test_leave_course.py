from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../leave_course.feature",
    "Leaving a joined course removes the student from the course",
)
def test_leave_course(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "student_ids") == []
