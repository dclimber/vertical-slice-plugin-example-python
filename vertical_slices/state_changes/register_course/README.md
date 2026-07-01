# register_course

This package contains the `state-change.register-course` slice.

Its responsibility is to handle the `course.register` command and emit
`CourseRegistered`.

Decision boundary:

- one new `CourseID`

Public interface:

- command: `course.register`
- slice class: `RegisterCourse`
- plugin: `register_course_plugin`

Colocated specification files:

- `register_course.feature`
- `tests/test_register_course.py`
