from __future__ import annotations

import ast
import importlib
from pathlib import Path

from course_slice import events as course_events
from enrolment_slice import events as enrolment_events
from student_slice import events as student_events

ROOT = Path(__file__).resolve().parents[2]

BROAD_DOMAIN_PACKAGE_FILES = (
    ROOT / "vertical_slices/student_slice/student_slice/slices.py",
    ROOT / "vertical_slices/course_slice/course_slice/slices.py",
    ROOT / "vertical_slices/enrolment_slice/enrolment_slice/slices.py",
    ROOT / "vertical_slices/enrolment_slice/enrolment_slice/queries.py",
)

STATE_CHANGE_AND_VIEW_FILES = tuple(
    sorted(
        path
        for root in (ROOT / "vertical_slices/state-changes", ROOT / "vertical_slices/state-views")
        for path in root.rglob("*.py")
    )
)

EXPECTED_CLASS_LOCATIONS = {
    "StudentRegistered": Path("vertical_slices/student_events/student_events/events.py"),
    "StudentNameUpdated": Path("vertical_slices/student_events/student_events/events.py"),
    "StudentMaxCoursesUpdated": Path("vertical_slices/student_events/student_events/events.py"),
    "CourseRegistered": Path("vertical_slices/courses_events/courses_events/events.py"),
    "CourseNameUpdated": Path("vertical_slices/courses_events/courses_events/events.py"),
    "CoursePlacesUpdated": Path("vertical_slices/courses_events/courses_events/events.py"),
    "StudentJoinedCourse": Path("vertical_slices/enrollment_events/enrollment_events/events.py"),
    "StudentLeftCourse": Path("vertical_slices/enrollment_events/enrollment_events/events.py"),
    "RegisterStudent": Path(
        "vertical_slices/state-changes/register_student/register_student/slice.py"
    ),
    "UpdateStudentName": Path(
        "vertical_slices/state-changes/update_student_name/update_student_name/slice.py"
    ),
    "UpdateMaxCourses": Path(
        "vertical_slices/state-changes/update_student_max_courses/update_student_max_courses/slice.py"
    ),
    "RegisterCourse": Path("vertical_slices/state-changes/register_course/register_course/slice.py"),
    "UpdateCourseName": Path(
        "vertical_slices/state-changes/update_course_name/update_course_name/slice.py"
    ),
    "UpdateCoursePlaces": Path(
        "vertical_slices/state-changes/update_course_places/update_course_places/slice.py"
    ),
    "StudentJoinsCourse": Path("vertical_slices/state-changes/join_course/join_course/slice.py"),
    "StudentLeavesCourse": Path("vertical_slices/state-changes/leave_course/leave_course/slice.py"),
    "StudentIDsForCourse": Path(
        "vertical_slices/state-views/student_ids_for_course/student_ids_for_course/view.py"
    ),
    "StudentNames": Path("vertical_slices/state-views/student_names/student_names/view.py"),
    "CourseIDsForStudent": Path(
        "vertical_slices/state-views/course_ids_for_student/course_ids_for_student/view.py"
    ),
    "CourseNames": Path("vertical_slices/state-views/course_names/course_names/view.py"),
    "Student": Path("vertical_slices/state-views/student_summary/student_summary/view.py"),
    "Course": Path("vertical_slices/state-views/course_summary/course_summary/view.py"),
}


def _class_definition_locations() -> dict[str, list[Path]]:
    locations: dict[str, list[Path]] = {}
    for path in ROOT.rglob("*.py"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        module = ast.parse(path.read_text())
        for node in module.body:
            if isinstance(node, ast.ClassDef):
                locations.setdefault(node.name, []).append(path.relative_to(ROOT))
    return locations


def test_durable_classes_are_defined_once_in_their_canonical_modules() -> None:
    class_locations = _class_definition_locations()

    assert {
        name: class_locations.get(name, [])
        for name in EXPECTED_CLASS_LOCATIONS
    } == {
        name: [path] for name, path in EXPECTED_CLASS_LOCATIONS.items()
    }


def test_event_compatibility_modules_re_export_canonical_event_objects() -> None:
    canonical_student_events = importlib.import_module("student_events.events")
    courses_events = importlib.import_module("courses_events.events")
    enrollment_events = importlib.import_module("enrollment_events.events")

    assert canonical_student_events.StudentRegistered is student_events.StudentRegistered
    assert canonical_student_events.StudentNameUpdated is student_events.StudentNameUpdated
    assert (
        canonical_student_events.StudentMaxCoursesUpdated
        is student_events.StudentMaxCoursesUpdated
    )
    assert courses_events.CourseRegistered is course_events.CourseRegistered
    assert courses_events.CourseNameUpdated is course_events.CourseNameUpdated
    assert courses_events.CoursePlacesUpdated is course_events.CoursePlacesUpdated
    assert enrollment_events.StudentJoinedCourse is enrolment_events.StudentJoinedCourse
    assert enrollment_events.StudentLeftCourse is enrolment_events.StudentLeftCourse


def test_broad_domain_packages_do_not_define_command_or_query_slice_classes() -> None:
    forbidden_class_names = {
        "RegisterStudent",
        "UpdateStudentName",
        "UpdateMaxCourses",
        "RegisterCourse",
        "UpdateCourseName",
        "UpdateCoursePlaces",
        "StudentJoinsCourse",
        "StudentLeavesCourse",
        "StudentIDsForCourse",
        "StudentNames",
        "CourseIDsForStudent",
        "CourseNames",
        "Student",
        "Course",
    }

    for path in BROAD_DOMAIN_PACKAGE_FILES:
        module = ast.parse(path.read_text())
        class_names = {
            node.name for node in ast.walk(module) if isinstance(node, ast.ClassDef)
        }
        assert forbidden_class_names.isdisjoint(class_names), path


def test_state_change_and_state_view_packages_do_not_define_durable_event_classes() -> None:
    durable_event_class_names = {
        "StudentRegistered",
        "StudentNameUpdated",
        "StudentMaxCoursesUpdated",
        "CourseRegistered",
        "CourseNameUpdated",
        "CoursePlacesUpdated",
        "StudentJoinedCourse",
        "StudentLeftCourse",
    }

    for path in STATE_CHANGE_AND_VIEW_FILES:
        module = ast.parse(path.read_text())
        class_names = {
            node.name for node in ast.walk(module) if isinstance(node, ast.ClassDef)
        }
        assert durable_event_class_names.isdisjoint(class_names), path
