from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

SliceFactory = Callable[..., Any]


@dataclass
class Registry:
    events: dict[str, type] = field(default_factory=dict)
    commands: dict[str, SliceFactory] = field(default_factory=dict)
    queries: dict[str, SliceFactory] = field(default_factory=dict)
    automations: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    consumed_events: set[str] = field(default_factory=set)

    def event(self, name: str, event_type: type, version: int = 1) -> None:
        del version
        self.events[name] = event_type

    def command(self, name: str, slice_factory: SliceFactory) -> None:
        self.commands[name] = slice_factory

    def query(self, name: str, slice_factory: SliceFactory) -> None:
        self.queries[name] = slice_factory

    def automation(
        self,
        name: str,
        *,
        consumed_events: list[str],
        query_dependencies: list[str],
        emitted_commands: list[str],
    ) -> None:
        self.automations[name] = {
            "consumed_events": consumed_events,
            "query_dependencies": query_dependencies,
            "emitted_commands": emitted_commands,
        }

    def consumes(self, event_name: str) -> None:
        self.consumed_events.add(event_name)


class SlicePlugin(Protocol):
    name: str

    def register(self, registry: Registry) -> None: ...


class AutomationPlugin(Protocol):
    name: str

    def register(self, registry: Registry) -> None: ...


@dataclass
class UseCase:
    name: str
    slices: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    queries: list[str] = field(default_factory=list)
    feature: str | None = None


@dataclass
class Composition:
    registry: Registry = field(default_factory=Registry)
    use_cases: dict[str, UseCase] = field(default_factory=dict)

    def use_case(self, name: str) -> UseCase:
        return self.use_cases.setdefault(name, UseCase(name=name))

    def validate(self) -> None:
        for use_case in self.use_cases.values():
            for command in use_case.commands:
                if command not in self.registry.commands:
                    raise RuntimeError(
                        f"Use case {use_case.name!r} requires missing command {command!r}"
                    )

            for query in use_case.queries:
                if query not in self.registry.queries:
                    raise RuntimeError(
                        f"Use case {use_case.name!r} requires missing query {query!r}"
                    )
