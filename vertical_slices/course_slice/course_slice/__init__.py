from __future__ import annotations

from course_slice.events import CourseNameUpdated, CoursePlacesUpdated, CourseRegistered
from course_slice.plugin import CourseSlicePlugin, course_slice
from course_slice.slices import (
    RegisterCourse,
    UpdateCourseName,
    UpdateCoursePlaces,
    UpdatePlaces,
)

__all__ = [
    "CourseNameUpdated",
    "CoursePlacesUpdated",
    "CourseRegistered",
    "CourseSlicePlugin",
    "RegisterCourse",
    "UpdateCourseName",
    "UpdateCoursePlaces",
    "UpdatePlaces",
    "course_slice",
]
