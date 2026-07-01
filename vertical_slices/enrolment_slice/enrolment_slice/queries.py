from __future__ import annotations

from course_ids_for_student.view import CourseIDsForStudent
from course_names.view import CourseNames
from course_summary.view import Course
from student_ids_for_course.view import StudentIDsForCourse
from student_names.view import StudentNames
from student_summary.view import Student

StudentsIDs = StudentIDsForCourse
CourseIDs = CourseIDsForStudent

__all__ = [
    "StudentIDsForCourse",
    "StudentsIDs",
    "StudentNames",
    "CourseIDsForStudent",
    "CourseIDs",
    "CourseNames",
    "Student",
    "Course",
]
