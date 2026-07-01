# courses_events

This package defines the canonical durable events for course state.

It owns:

- `CourseID`
- `CourseRegistered`
- `CourseNameUpdated`
- `CoursePlacesUpdated`

Other slices may import these types, but they should not redefine them.
This package contains shared event contracts only. It does not register
commands, answer queries, or implement decision logic.
