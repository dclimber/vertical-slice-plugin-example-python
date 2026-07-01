# student_ids_for_course

This package contains the `state-view.student-ids-for-course` slice.

Its responsibility is to answer which students are currently enrolled on one
course by projecting enrollment events for that `CourseID`.

Projection pattern:

- consume `StudentJoinedCourse`
- consume `StudentLeftCourse`
- expose current `student_ids`

Public interface:

- queries: `enrollment.student_ids_for_course`, `enrolment.student_ids_for_course`
- view class: `StudentIDsForCourse`
- plugin: `student_ids_for_course_plugin`

Colocated specification files:

- `student_ids_for_course.feature`
- `tests/test_student_ids_for_course.py`
