from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../student_ids_for_course.feature",
    "Querying student IDs for a course returns current enrolled students",
)
def test_student_ids_for_course(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    student_id = bdd_context["vars"]["student_id"]
    assert getattr(result, "student_ids") == [student_id]
