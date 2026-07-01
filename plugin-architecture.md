# Architecture Notes

This repo explores one way to structure a Python event-sourced DCB application
around explicit vertical slice package boundaries.

## Package Taxonomy

```text
vertical_slices/student_events      shared student event contracts
vertical_slices/courses_events      shared course event contracts
vertical_slices/enrollment_events   shared enrollment event contracts
vertical_slices/state-changes       command -> event slices
vertical_slices/state-views         event -> query/read-model slices
vertical_slices/automations         future automation packages
docs/features                       flow/use-case specifications
tests/bdd                           executable flow/use-case specifications
```

## Composition

`src/course_app/use_cases.py` is the composition root. It registers durable
events from the shared contract packages, then wires command and query plugins
into use cases.

Examples:

- `student.register` uses `state-change.register-student`
- `course.register` uses `state-change.register-course`
- `enrolment.student_joins_course` uses `state-change.register-student`,
  `state-change.register-course`, `state-change.join-course`,
  `state-view.student-ids-for-course`, and `state-view.student-names`

## Responsibilities

Event packages define shared contracts. They are stable durable event types that
other slices can import.

State-change packages are command -> event slices. Each one owns a decision
boundary and emits durable events.

State-view packages are event -> query/read-model slices. Each one projects
events into a query response or read model.

Automation packages are reserved for event -> read model -> automatic process ->
command -> event pipelines. There is no domain automation in the current
example.

BDD features describe flows and use cases. They prove the composition without
turning feature files into slice packages.

Compatibility import surfaces remain for the original
`EnrolmentWithVerticalSlices` API. They re-export canonical classes from the
package taxonomy above.
