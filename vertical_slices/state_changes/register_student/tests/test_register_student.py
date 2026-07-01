from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../register_student.feature",
    "Registering a student records the student details",
)
def test_register_student(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "name") == "Alice"
    assert getattr(result, "max_courses") == 3
    assert getattr(result, "course_ids") == []
