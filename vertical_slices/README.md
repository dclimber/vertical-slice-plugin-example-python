# vertical_slices

This directory holds the canonical package layout for the example domain.

Its purpose is to make the DCB application structure explicit:

- event packages define durable shared contracts
- state-change packages implement `command -> event` slices
- state-view packages implement `event -> query/read model` slices
- automation packages are reserved for future `event -> read model -> command -> event` flows

The production application composes these packages from `src/course_app/`.
Tests treat this directory as the primary architectural surface of the repo.
