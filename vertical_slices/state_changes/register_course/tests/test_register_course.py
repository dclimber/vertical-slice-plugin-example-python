from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../register_course.feature",
    "Registering a course records the course details",
)
def test_register_course(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "name") == "Maths"
    assert getattr(result, "places") == 2
    assert getattr(result, "student_ids") == []
