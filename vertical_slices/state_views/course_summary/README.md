# course_summary

This package contains the `state-view.course-summary` slice.

Its responsibility is to project the current summary for one course,
including name, place count, and joined student IDs.

Projection pattern:

- consume `CourseRegistered`
- consume `CourseNameUpdated`
- consume `CoursePlacesUpdated`
- consume `StudentJoinedCourse`
- consume `StudentLeftCourse`

Public interface:

- queries: `enrollment.course`, `enrolment.course`
- view class: `Course`
- plugin: `course_summary_plugin`

Colocated specification files:

- `course_summary.feature`
- `tests/test_course_summary.py`
