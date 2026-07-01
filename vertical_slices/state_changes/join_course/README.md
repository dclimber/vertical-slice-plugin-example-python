# join_course

This package contains the `state-change.join-course` slice.

Its responsibility is to handle the `enrollment.join_course` and
`enrolment.join_course` commands and emit `StudentJoinedCourse` when the
student and course satisfy the enrollment rules.

Decision boundary:

- student registration and enrollment history for one `StudentID`
- course registration and enrollment history for one `CourseID`

Business rules enforced here:

- student must exist
- course must exist
- course must have free places
- student must be under the max course limit
- student must not already be on the course

Public interface:

- commands: `enrollment.join_course`, `enrolment.join_course`
- slice class: `StudentJoinsCourse`
- plugin: `join_course_plugin`

Colocated specification files:

- `join_course.feature`
- `tests/test_join_course.py`
