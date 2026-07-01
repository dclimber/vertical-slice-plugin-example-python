from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../update_course_places.feature",
    "Updating a registered course places changes the course summary",
)
def test_update_course_places(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "places") == 5
