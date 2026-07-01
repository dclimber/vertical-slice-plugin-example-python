from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../update_student_max_courses.feature",
    "Updating a registered student's course limit changes the student summary",
)
def test_update_student_max_courses(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "max_courses") == 5
