from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../join_course.feature",
    "Joining a course adds the student to the course",
)
def test_join_course(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    student_id = bdd_context["vars"]["student_id"]
    assert getattr(result, "student_ids") == [student_id]
