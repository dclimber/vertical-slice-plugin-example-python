from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../student_summary.feature",
    "Querying a student summary returns the current student state",
)
def test_student_summary(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    course_id = bdd_context["vars"]["course_id"]
    assert getattr(result, "name") == "Ada"
    assert getattr(result, "max_courses") == 3
    assert getattr(result, "course_ids") == [course_id]
