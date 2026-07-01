from __future__ import annotations

from typing import NewType, Protocol


StudentID = NewType("StudentID", str)
CourseID = NewType("CourseID", str)


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


class StudentView(Protocol):
    student_id: StudentID
    name: str
    max_courses: int
    course_ids: list[CourseID]


class CourseView(Protocol):
    course_id: CourseID
    name: str
    places: int
    student_ids: list[StudentID]


class EnrolmentInterface(Protocol):
    def register_student(self, name: str, max_courses: int) -> StudentID: ...

    def register_course(self, name: str, places: int) -> CourseID: ...

    def join_course(self, student_id: StudentID, course_id: CourseID) -> None: ...

    def leave_course(self, student_id: StudentID, course_id: CourseID) -> None: ...

    def list_students_for_course(self, course_id: CourseID) -> list[str]: ...

    def list_courses_for_student(self, student_id: StudentID) -> list[str]: ...

    def update_student_name(self, student_id: StudentID, name: str) -> None: ...

    def update_max_courses(self, student_id: StudentID, max_courses: int) -> None: ...

    def update_course_name(self, course_id: CourseID, name: str) -> None: ...

    def update_places(self, course_id: CourseID, places: int) -> None: ...

    def get_student(self, student_id: StudentID) -> StudentView: ...

    def get_course(self, course_id: CourseID) -> CourseView: ...
