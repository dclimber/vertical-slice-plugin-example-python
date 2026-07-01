# student_names

This package contains the `state-view.student-names` slice.

Its responsibility is to answer the current names for a supplied list of
students by projecting student registration and rename events.

Projection pattern:

- consume `StudentRegistered`
- consume `StudentNameUpdated`
- expose current `names`

Public interface:

- queries: `enrollment.student_names`, `enrolment.student_names`
- view class: `StudentNames`
- plugin: `student_names_plugin`

Colocated specification files:

- `student_names.feature`
- `tests/test_student_names.py`
