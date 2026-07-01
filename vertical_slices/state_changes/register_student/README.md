# register_student

This package contains the `state-change.register-student` slice.

Its responsibility is to handle the `student.register` command and emit
`StudentRegistered`.

Decision boundary:

- one new `StudentID`

Public interface:

- command: `student.register`
- slice class: `RegisterStudent`
- plugin: `register_student_plugin`

Colocated specification files:

- `register_student.feature`
- `tests/test_register_student.py`
