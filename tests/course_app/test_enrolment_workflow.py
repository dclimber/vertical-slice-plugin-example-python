from __future__ import annotations

import pytest

from enrollment_events.errors import (
    CourseNotFoundError,
    FullyBookedError,
    NotAlreadyJoinedError,
    StudentNotFoundError,
    TooManyCoursesError,
)

from course_app.main import create_app


def test_course_app_runs_the_enrolment_workflow() -> None:
    app = create_app(
        env={
            "PERSISTENCE_MODULE": "eventsourcing.dcb.popo",
        }
    )

    missing_student_id = "student-missing"
    missing_course_id = "course-missing"

    with pytest.raises(CourseNotFoundError):
        app.join_course(student_id=missing_student_id, course_id=missing_course_id)

    student_id = app.register_student(name="Alice", max_courses=1)
    course_id = app.register_course(name="Maths", places=1)

    student = app.get_student(student_id)
    assert student.student_id == student_id
    assert student.name == "Alice"
    assert student.max_courses == 1
    assert student.course_ids == []

    course = app.get_course(course_id)
    assert course.course_id == course_id
    assert course.name == "Maths"
    assert course.places == 1
    assert course.student_ids == []

    with pytest.raises(CourseNotFoundError):
        app.join_course(student_id=student_id, course_id=missing_course_id)

    with pytest.raises(StudentNotFoundError):
        app.join_course(student_id=missing_student_id, course_id=course_id)

    app.join_course(student_id=student_id, course_id=course_id)

    student = app.get_student(student_id)
    course = app.get_course(course_id)
    assert student.course_ids == [course_id]
    assert course.student_ids == [student_id]
    assert app.list_students_for_course(course_id) == ["Alice"]
    assert app.list_courses_for_student(student_id) == ["Maths"]

    other_student_id = app.register_student(name="Bob", max_courses=1)
    with pytest.raises(FullyBookedError):
        app.join_course(student_id=other_student_id, course_id=course_id)

    second_course_id = app.register_course(name="Science", places=1)
    with pytest.raises(TooManyCoursesError):
        app.join_course(student_id=student_id, course_id=second_course_id)

    app.leave_course(student_id=student_id, course_id=course_id)

    with pytest.raises(NotAlreadyJoinedError):
        app.leave_course(student_id=student_id, course_id=course_id)
