from __future__ import annotations

from pytest_bdd import scenario


@scenario(
    "../student_names.feature",
    "Querying student names returns the current student names",
)
def test_student_names(bdd_context: dict[str, object]) -> None:
    result = bdd_context["last_result"]
    assert getattr(result, "names") == ["Alice", "Robert"]
