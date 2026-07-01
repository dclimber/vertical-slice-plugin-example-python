from __future__ import annotations

from typing import NewType

from eventsourcing.dcb.msgpack import Decision

CourseID = NewType("CourseID", str)

__all__ = [
    "CourseID",
    "CourseRegistered",
    "CourseNameUpdated",
    "CoursePlacesUpdated",
]


class CourseRegistered(Decision):
    course_id: CourseID
    name: str
    places: int


class CourseNameUpdated(Decision):
    course_id: CourseID
    name: str


class CoursePlacesUpdated(Decision):
    course_id: CourseID
    places: int
