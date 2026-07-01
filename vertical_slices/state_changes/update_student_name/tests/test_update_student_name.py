from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../update_student_name.feature",
    "Updating a registered student's name changes the student summary",
)
def test_update_student_name(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "name") == "Ada"
