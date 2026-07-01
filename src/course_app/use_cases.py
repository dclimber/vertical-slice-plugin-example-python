from __future__ import annotations

from courses_events.events import CourseNameUpdated, CoursePlacesUpdated, CourseRegistered
from course_ids_for_student.plugin import course_ids_for_student_plugin
from course_names.plugin import course_names_plugin
from course_summary.plugin import course_summary_plugin
from enrollment_events.events import StudentJoinedCourse, StudentLeftCourse
from join_course.plugin import join_course_plugin
from leave_course.plugin import leave_course_plugin
from register_course.plugin import register_course_plugin
from register_student.plugin import register_student_plugin
from student_ids_for_course.plugin import student_ids_for_course_plugin
from student_names.plugin import student_names_plugin
from student_summary.plugin import student_summary_plugin
from student_events.events import (
    StudentMaxCoursesUpdated,
    StudentNameUpdated,
    StudentRegistered,
)
from update_course_name.plugin import update_course_name_plugin
from update_course_places.plugin import update_course_places_plugin
from update_student_max_courses.plugin import update_student_max_courses_plugin
from update_student_name.plugin import update_student_name_plugin

from course_app.app import CourseApp


def register_use_cases(app: CourseApp) -> None:
    registry = app.composition.registry

    registry.event("student.registered", StudentRegistered, version=1)
    registry.event("student.name_updated", StudentNameUpdated, version=1)
    registry.event("student.max_courses_updated", StudentMaxCoursesUpdated, version=1)
    registry.event("course.registered", CourseRegistered, version=1)
    registry.event("course.name_updated", CourseNameUpdated, version=1)
    registry.event("course.places_updated", CoursePlacesUpdated, version=1)
    registry.event("enrolment.student_joined_course", StudentJoinedCourse, version=1)
    registry.event("enrolment.student_left_course", StudentLeftCourse, version=1)

    registry.consumes("student.registered")
    registry.consumes("student.name_updated")
    registry.consumes("student.max_courses_updated")
    registry.consumes("course.registered")
    registry.consumes("course.name_updated")
    registry.consumes("course.places_updated")

    register_student_plugin.register(registry)
    update_student_name_plugin.register(registry)
    update_student_max_courses_plugin.register(registry)
    register_course_plugin.register(registry)
    update_course_name_plugin.register(registry)
    update_course_places_plugin.register(registry)
    join_course_plugin.register(registry)
    leave_course_plugin.register(registry)
    student_ids_for_course_plugin.register(registry)
    student_names_plugin.register(registry)
    course_ids_for_student_plugin.register(registry)
    course_names_plugin.register(registry)
    student_summary_plugin.register(registry)
    course_summary_plugin.register(registry)

    register_student = app.composition.use_case("student.register")
    register_student.slices = ["state-change.register-student"]
    register_student.commands = ["student.register"]

    register_course = app.composition.use_case("course.register")
    register_course.slices = ["state-change.register-course"]
    register_course.commands = ["course.register"]

    student_joins_course = app.composition.use_case("enrolment.student_joins_course")
    student_joins_course.slices = [
        "state-change.register-student",
        "state-change.register-course",
        "state-change.join-course",
        "state-view.student-ids-for-course",
        "state-view.student-names",
    ]
    student_joins_course.commands = [
        "student.register",
        "course.register",
        "enrollment.join_course",
    ]
    student_joins_course.queries = [
        "enrollment.student_ids_for_course",
        "enrollment.student_names",
    ]

    student_leaves_course = app.composition.use_case("enrolment.student_leaves_course")
    student_leaves_course.slices = [
        "state-change.leave-course",
        "state-view.course-summary",
        "state-view.student-summary",
    ]
    student_leaves_course.commands = ["enrollment.leave_course"]
    student_leaves_course.queries = ["enrollment.course", "enrollment.student"]

    app.composition.validate()
