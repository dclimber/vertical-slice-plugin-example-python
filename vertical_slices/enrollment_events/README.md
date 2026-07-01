# enrollment_events

This package defines the canonical durable events and domain errors for
student-course enrollment state.

It owns:

- `StudentJoinedCourse`
- `StudentLeftCourse`
- `StudentNotFoundError`
- `CourseNotFoundError`
- `AlreadyJoinedError`
- `NotAlreadyJoinedError`
- `FullyBookedError`
- `TooManyCoursesError`

The event types are shared contracts used by state-change and state-view
slices. The error types capture enrollment-specific business rule failures.
This package does not register commands or queries by itself.
