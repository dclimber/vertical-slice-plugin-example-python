from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../update_course_name.feature",
    "Updating a registered course name changes the course summary",
)
def test_update_course_name(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "name") == "Physics"
