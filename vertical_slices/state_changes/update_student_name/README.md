# update_student_name

This package contains the `state-change.update-student-name` slice.

Its responsibility is to handle the `student.update_name` command and emit
`StudentNameUpdated` for an already-registered student.

Decision boundary:

- prior student registration events for one `StudentID`

Public interface:

- command: `student.update_name`
- slice class: `UpdateStudentName`
- plugin: `update_student_name_plugin`

Colocated specification files:

- `update_student_name.feature`
- `tests/test_update_student_name.py`
