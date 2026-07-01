from __future__ import annotations


class StudentNotFoundError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


class AlreadyJoinedError(Exception):
    pass


class NotAlreadyJoinedError(Exception):
    pass


class FullyBookedError(Exception):
    pass


class TooManyCoursesError(Exception):
    pass
