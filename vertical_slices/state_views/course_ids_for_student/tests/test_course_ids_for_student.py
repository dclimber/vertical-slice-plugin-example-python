from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../course_ids_for_student.feature",
    "Querying course IDs for a student returns current joined courses",
)
def test_course_ids_for_student(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    course_1 = bdd_context["vars"]["course_1"]
    course_2 = bdd_context["vars"]["course_2"]
    assert getattr(result, "course_ids") == [course_1, course_2]
