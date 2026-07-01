# vertical_slices

`vertical_slices` is a learning and brainstorming repo about structuring a
Python event-sourced DCB application as small, composable vertical slices.

The example domain is course enrolment. The repo explores how a compact DCB
application can be split into explicit event contracts, command slices,
read-model slices, use-case composition, and BDD flow specifications.

## What This Explores

- Durable event packages as shared contracts.
- State-change slices as `command -> event` packages.
- State-view slices as `event -> query/read model` packages.
- Automation slices as a future `event -> read model -> command -> event`
  extension point.
- BDD features as flow/use-case specs rather than slice packages.
- A small application API for running the enrolment workflow directly.

This is intentionally an exploration, not a production template. The value is in
the package boundaries, tests, and tradeoffs.

## Layout

```text
vertical_slices/student_events       durable student event contracts
vertical_slices/courses_events       durable course event contracts
vertical_slices/enrollment_events    durable enrollment event contracts
vertical_slices/state-changes        command -> event slices
vertical_slices/state-views          event -> query/read-model slices
vertical_slices/automations          placeholder for future automation packages

src/course_app                       application API and explicit composition root
docs/features                        Gherkin flow specs
tests                                contract, architecture, BDD, and composition tests
```

The `student_slice`, `course_slice`, and `enrolment_slice` packages are
domain-area import shims. They re-export canonical classes from the slice
packages so the domain can still be browsed at a higher level.

## Composition

`src/course_app/use_cases.py` registers canonical events and composes use cases
from the smaller slice packages.

Examples:

- `student.register` uses `state-change.register-student`
- `course.register` uses `state-change.register-course`
- `enrolment.student_joins_course` composes:
  `state-change.register-student`,
  `state-change.register-course`,
  `state-change.join-course`,
  `state-view.student-ids-for-course`,
  `state-view.student-names`

## Run It

Install and run checks with `uv`:

```bash
uv sync
uv run ruff check .
uv run pytest
```

If your environment needs a writable cache location:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ruff check .
UV_CACHE_DIR=/tmp/uv-cache uv run pytest
```

## AI Assistance Disclosure

This repository was developed as an AI-assisted learning exercise. The code and
docs were written through iterative prompting and review with GPT-5-family
models, with the repository author directing the architecture, cleanup, and
final publishing decisions.

Treat the code as study material: read the tests, inspect the boundaries, and
adapt the ideas deliberately before using them in a real system.

## License

This project is licensed under the BSD 3-Clause License. Redistributions must
retain the copyright notice and license text.
