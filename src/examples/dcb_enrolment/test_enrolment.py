from __future__ import annotations

from unittest import TestCase

from examples.dcb_enrolment.interface import (
    CourseNotFoundError,
    EnrolmentInterface,
    FullyBookedError,
    NotAlreadyJoinedError,
    StudentNotFoundError,
    TooManyCoursesError,
)


class EnrolmentTestCase(TestCase):
    def assert_implementation(self, app: EnrolmentInterface) -> None:
        missing_student_id = "student-missing"
        missing_course_id = "course-missing"

        with self.assertRaises(CourseNotFoundError):
            app.join_course(student_id=missing_student_id, course_id=missing_course_id)

        student_id = app.register_student(name="Alice", max_courses=1)
        course_id = app.register_course(name="Maths", places=1)

        student = app.get_student(student_id)
        self.assertEqual(student_id, student.student_id)
        self.assertEqual("Alice", student.name)
        self.assertEqual(1, student.max_courses)
        self.assertEqual([], student.course_ids)

        course = app.get_course(course_id)
        self.assertEqual(course_id, course.course_id)
        self.assertEqual("Maths", course.name)
        self.assertEqual(1, course.places)
        self.assertEqual([], course.student_ids)

        with self.assertRaises(CourseNotFoundError):
            app.join_course(student_id=student_id, course_id=missing_course_id)

        with self.assertRaises(StudentNotFoundError):
            app.join_course(student_id=missing_student_id, course_id=course_id)

        app.join_course(student_id=student_id, course_id=course_id)

        with self.assertRaises(FullyBookedError):
            app.join_course(student_id=student_id, course_id=course_id)

        student = app.get_student(student_id)
        course = app.get_course(course_id)
        self.assertEqual([course_id], student.course_ids)
        self.assertEqual([student_id], course.student_ids)

        self.assertEqual(["Alice"], app.list_students_for_course(course_id))
        self.assertEqual(["Maths"], app.list_courses_for_student(student_id))

        other_student_id = app.register_student(name="Bob", max_courses=1)
        with self.assertRaises(FullyBookedError):
            app.join_course(student_id=other_student_id, course_id=course_id)

        second_course_id = app.register_course(name="Science", places=1)
        with self.assertRaises(TooManyCoursesError):
            app.join_course(student_id=student_id, course_id=second_course_id)

        app.leave_course(student_id=student_id, course_id=course_id)

        with self.assertRaises(NotAlreadyJoinedError):
            app.leave_course(student_id=student_id, course_id=course_id)
