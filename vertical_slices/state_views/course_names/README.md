# course_names

This package contains the `state-view.course-names` slice.

Its responsibility is to answer the current names for a supplied list of
courses by projecting course registration and rename events.

Projection pattern:

- consume `CourseRegistered`
- consume `CourseNameUpdated`
- expose current `names`

Public interface:

- queries: `enrollment.course_names`, `enrolment.course_names`
- view class: `CourseNames`
- plugin: `course_names_plugin`

Colocated specification files:

- `course_names.feature`
- `tests/test_course_names.py`
