# student_summary

This package contains the `state-view.student-summary` slice.

Its responsibility is to project the current summary for one student,
including name, max course count, and joined course IDs.

Projection pattern:

- consume `StudentRegistered`
- consume `StudentNameUpdated`
- consume `StudentMaxCoursesUpdated`
- consume `StudentJoinedCourse`
- consume `StudentLeftCourse`

Public interface:

- queries: `enrollment.student`, `enrolment.student`
- view class: `Student`
- plugin: `student_summary_plugin`

Colocated specification files:

- `student_summary.feature`
- `tests/test_student_summary.py`
