# update_student_max_courses

This package contains the `state-change.update-student-max-courses` slice.

Its responsibility is to handle the `student.update_max_courses` command and
emit `StudentMaxCoursesUpdated` for an already-registered student.

Decision boundary:

- prior student registration events for one `StudentID`

Public interface:

- command: `student.update_max_courses`
- slice class: `UpdateMaxCourses`
- plugin: `update_student_max_courses_plugin`

Colocated specification files:

- `update_student_max_courses.feature`
- `tests/test_update_student_max_courses.py`
