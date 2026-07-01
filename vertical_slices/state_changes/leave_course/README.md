# leave_course

This package contains the `state-change.leave-course` slice.

Its responsibility is to handle the `enrollment.leave_course` and
`enrolment.leave_course` commands and emit `StudentLeftCourse` when the
student is currently enrolled on the course.

Decision boundary:

- student registration and enrollment history for one `StudentID`
- course registration and enrollment history for one `CourseID`

Business rules enforced here:

- student must exist
- course must exist
- student must already be on the course

Public interface:

- commands: `enrollment.leave_course`, `enrolment.leave_course`
- slice class: `StudentLeavesCourse`
- plugin: `leave_course_plugin`

Colocated specification files:

- `leave_course.feature`
- `tests/test_leave_course.py`
