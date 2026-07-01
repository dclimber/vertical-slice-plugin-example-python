from __future__ import annotations

from collections.abc import Sequence

from course_slice.events import CourseNameUpdated, CoursePlacesUpdated, CourseRegistered
from course_slice.slices import RegisterCourse, UpdateCourseName, UpdatePlaces
from enrolment_slice.events import StudentJoinedCourse, StudentLeftCourse
from enrolment_slice.queries import (
    Course,
    CourseIDs,
    CourseNames,
    Student,
    StudentNames,
    StudentsIDs,
)
from enrolment_slice.slices import StudentJoinsCourse, StudentLeavesCourse
from eventsourcing.dcb.msgpack import Decision
from examples.dcb_enrolment.interface import (
    CourseID,
    EnrolmentInterface,
    StudentID,
)
from student_slice.events import (
    StudentMaxCoursesUpdated,
    StudentNameUpdated,
    StudentRegistered,
)
from student_slice.slices import RegisterStudent, UpdateMaxCourses, UpdateStudentName

from course_app.app import CourseApp
from course_app.use_cases import register_use_cases


class EnrolmentWithVerticalSlices(CourseApp, EnrolmentInterface):
    def __init__(self, env: dict[str, str] | None = None) -> None:
        super().__init__(env)
        register_use_cases(self)

    def register_student(self, name: str, max_courses: int) -> StudentID:
        result = self.handle_command(
            "student.register",
            name=name,
            max_courses=max_courses,
        )
        return result.student_id

    def register_course(self, name: str, places: int) -> CourseID:
        result = self.handle_command(
            "course.register",
            name=name,
            places=places,
        )
        return result.course_id

    def join_course(self, student_id: StudentID, course_id: CourseID) -> None:
        self.handle_command(
            "enrolment.join_course",
            student_id=student_id,
            course_id=course_id,
        )

    def leave_course(self, student_id: StudentID, course_id: CourseID) -> None:
        self.handle_command(
            "enrolment.leave_course",
            student_id=student_id,
            course_id=course_id,
        )

    def list_students_for_course(self, course_id: CourseID) -> list[str]:
        student_ids = self.handle_query(
            "enrollment.student_ids_for_course",
            course_id=course_id,
        ).student_ids
        return self.handle_query(
            "enrollment.student_names",
            student_ids=student_ids,
        ).names

    def list_courses_for_student(self, student_id: StudentID) -> list[str]:
        course_ids = self.handle_query(
            "enrollment.course_ids_for_student",
            student_id=student_id,
        ).course_ids
        return self.handle_query(
            "enrollment.course_names",
            course_ids=course_ids,
        ).names

    def update_student_name(self, student_id: StudentID, name: str) -> None:
        self.handle_command(
            "student.update_name",
            student_id=student_id,
            name=name,
        )

    def update_max_courses(self, student_id: StudentID, max_courses: int) -> None:
        self.handle_command(
            "student.update_max_courses",
            student_id=student_id,
            max_courses=max_courses,
        )

    def update_course_name(self, course_id: CourseID, name: str) -> None:
        self.handle_command(
            "course.update_name",
            course_id=course_id,
            name=name,
        )

    def update_places(self, course_id: CourseID, places: int) -> None:
        self.handle_command(
            "course.update_places",
            course_id=course_id,
            places=places,
        )

    def get_student(self, student_id: StudentID) -> Student:
        return self.handle_query("enrollment.student", student_id=student_id)

    def get_course(self, course_id: CourseID) -> Course:
        return self.handle_query("enrollment.course", course_id=course_id)


DecisionTypes = Sequence[type[Decision]]

__all__ = [
    "Course",
    "CourseID",
    "CourseIDs",
    "CourseNameUpdated",
    "CourseNames",
    "CoursePlacesUpdated",
    "CourseRegistered",
    "DecisionTypes",
    "EnrolmentInterface",
    "EnrolmentWithVerticalSlices",
    "RegisterCourse",
    "RegisterStudent",
    "Student",
    "StudentID",
    "StudentJoinedCourse",
    "StudentJoinsCourse",
    "StudentLeftCourse",
    "StudentLeavesCourse",
    "StudentMaxCoursesUpdated",
    "StudentNameUpdated",
    "StudentNames",
    "StudentRegistered",
    "StudentsIDs",
    "UpdateCourseName",
    "UpdateMaxCourses",
    "UpdatePlaces",
    "UpdateStudentName",
]
