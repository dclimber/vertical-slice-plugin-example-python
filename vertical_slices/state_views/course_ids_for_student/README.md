# course_ids_for_student

This package contains the `state-view.course-ids-for-student` slice.

Its responsibility is to answer which courses a student is currently enrolled
on by projecting enrollment events for that `StudentID`.

Projection pattern:

- consume `StudentJoinedCourse`
- consume `StudentLeftCourse`
- expose current `course_ids`

Public interface:

- queries: `enrollment.course_ids_for_student`, `enrolment.course_ids_for_student`
- view class: `CourseIDsForStudent`
- plugin: `course_ids_for_student_plugin`

Colocated specification files:

- `course_ids_for_student.feature`
- `tests/test_course_ids_for_student.py`
