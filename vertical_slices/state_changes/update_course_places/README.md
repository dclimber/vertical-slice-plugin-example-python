# update_course_places

This package contains the `state-change.update-course-places` slice.

Its responsibility is to handle the `course.update_places` command and emit
`CoursePlacesUpdated` for an already-registered course.

Decision boundary:

- prior course registration events for one `CourseID`

Public interface:

- command: `course.update_places`
- slice class: `UpdateCoursePlaces`
- plugin: `update_course_places_plugin`

Colocated specification files:

- `update_course_places.feature`
- `tests/test_update_course_places.py`
