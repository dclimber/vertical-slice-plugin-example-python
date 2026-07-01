from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../course_summary.feature",
    "Querying a course summary returns the current course state",
)
def test_course_summary(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    student_id = bdd_context["vars"]["student_id"]
    assert getattr(result, "name") == "Physics"
    assert getattr(result, "places") == 3
    assert getattr(result, "student_ids") == [student_id]
