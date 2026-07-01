from __future__ import annotations

from dataclasses import dataclass

import pytest

from course_kernel.composition import Composition


def test_validate_fails_when_use_case_references_missing_command() -> None:
    composition = Composition()
    composition.use_case("student.register").commands.append("student.register")

    with pytest.raises(
        RuntimeError,
        match="Use case 'student.register' requires missing command 'student.register'",
    ):
        composition.validate()


def test_validate_fails_when_use_case_references_missing_query() -> None:
    composition = Composition()
    composition.use_case("enrolment.student").queries.append("enrolment.student")

    with pytest.raises(
        RuntimeError,
        match="Use case 'enrolment.student' requires missing query 'enrolment.student'",
    ):
        composition.validate()


def test_registry_tracks_registered_events_commands_queries_and_consumers() -> None:
    composition = Composition()

    class ExampleEvent:
        pass

    def command_factory() -> object:
        return object()

    def query_factory() -> object:
        return object()

    composition.registry.event("example.happened", ExampleEvent, version=1)
    composition.registry.command("example.command", command_factory)
    composition.registry.query("example.query", query_factory)
    composition.registry.consumes("example.happened")

    assert composition.registry.events == {"example.happened": ExampleEvent}
    assert composition.registry.commands == {"example.command": command_factory}
    assert composition.registry.queries == {"example.query": query_factory}
    assert composition.registry.consumed_events == {"example.happened"}


def test_automation_plugins_register_separately_from_commands_and_queries() -> None:
    composition = Composition()

    @dataclass
    class ExampleAutomationPlugin:
        name: str = "automation.sync-student-summary"

        def register(self, registry) -> None:
            registry.automation(
                self.name,
                consumed_events=["student.registered", "student.name_updated"],
                query_dependencies=["enrollment.student"],
                emitted_commands=["student.update_name"],
            )

    ExampleAutomationPlugin().register(composition.registry)

    assert composition.registry.commands == {}
    assert composition.registry.queries == {}
    assert composition.registry.automations == {
        "automation.sync-student-summary": {
            "consumed_events": [
                "student.registered",
                "student.name_updated",
            ],
            "query_dependencies": ["enrollment.student"],
            "emitted_commands": ["student.update_name"],
        }
    }
