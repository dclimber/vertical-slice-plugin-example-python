from __future__ import annotations

import json
from typing import Protocol, cast

from pytest_bdd import parsers, then

from tests.bdd.steps.command_steps import BddContext, Variables, interpolate


class QueryHandlingApp(Protocol):
    def handle_query(self, name: str, /, **kwargs: object) -> object: ...


@then(parsers.parse('query "{query_name}" with:'))
def query_with(
    app: QueryHandlingApp,
    bdd_context: BddContext,
    query_name: str,
    docstring: str,
) -> None:
    variables = cast(Variables, bdd_context["vars"])
    payload = cast(
        dict[str, object],
        interpolate(json.loads(docstring), variables),
    )
    result = app.handle_query(query_name, **payload)
    bdd_context["last_result"] = result


@then(parsers.parse('should have field "{field_name}" equal to:'))
def should_have_field_equal_to(
    bdd_context: BddContext,
    field_name: str,
    docstring: str,
) -> None:
    variables = cast(Variables, bdd_context["vars"])
    expected = interpolate(json.loads(docstring), variables)
    actual = getattr(bdd_context["last_result"], field_name)
    assert actual == expected
