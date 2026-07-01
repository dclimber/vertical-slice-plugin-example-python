# Automations

This directory is reserved for automation packages.

An automation is not a state-change slice and not a state-view slice. It sits on
the pipeline `event -> read model -> automatic process -> command -> event`.

When the first real automation is added, give it its own package under
`vertical_slices/automations/` and register:

- consumed event names
- read model or query dependencies
- emitted command names

Automation packages may depend on canonical event packages and on read models or
query slices they need to inspect before emitting commands.

Translation slices remain separate from automations. They are the future
extension point for external inputs and follow
`external event -> automatic process -> command -> event`.
