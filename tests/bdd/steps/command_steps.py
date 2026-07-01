from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Protocol, TypeAlias, cast

from pytest_bdd import given, parsers, when

JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)
Variables: TypeAlias = dict[str, object]
BddContext: TypeAlias = dict[str, object]


class CommandHandlingApp(Protocol):
    def handle_command(self, name: str, /, **kwargs: object) -> object: ...


def interpolate(value: JsonValue, variables: Mapping[str, object]) -> JsonValue:
    if isinstance(value, str) and value.startswith("$"):
        variable_name = value[1:]
        if variable_name in variables:
            return cast(JsonValue, variables[variable_name])
        return value

    if isinstance(value, dict):
        return {key: interpolate(item, variables) for key, item in value.items()}

    if isinstance(value, list):
        return [interpolate(item, variables) for item in value]

    return value


@given(parsers.parse('command "{command_name}" succeeds with:'))
@when(parsers.parse('command "{command_name}" succeeds with:'))
def command_succeeds(
    app: CommandHandlingApp,
    bdd_context: BddContext,
    command_name: str,
    docstring: str,
) -> None:
    variables = cast(Variables, bdd_context["vars"])
    payload = cast(
        dict[str, object],
        interpolate(json.loads(docstring), variables),
    )
    result = app.handle_command(command_name, **payload)
    bdd_context["last_result"] = result


@given(parsers.parse('I remember result field "{field_name}" as "{variable_name}"'))
def remember_result_field(
    bdd_context: BddContext,
    field_name: str,
    variable_name: str,
) -> None:
    result = bdd_context["last_result"]
    variables = cast(Variables, bdd_context["vars"])
    variables[variable_name] = getattr(result, field_name)
