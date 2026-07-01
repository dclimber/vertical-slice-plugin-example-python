from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../course_names.feature",
    "Querying course names returns the current course names",
)
def test_course_names(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "names") == ["Maths", "Physics"]
