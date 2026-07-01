# update_course_name

This package contains the `state-change.update-course-name` slice.

Its responsibility is to handle the `course.update_name` command and emit
`CourseNameUpdated` for an already-registered course.

Decision boundary:

- prior course registration events for one `CourseID`

Public interface:

- command: `course.update_name`
- slice class: `UpdateCourseName`
- plugin: `update_course_name_plugin`

Colocated specification files:

- `update_course_name.feature`
- `tests/test_update_course_name.py`
