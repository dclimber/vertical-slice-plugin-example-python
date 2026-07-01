from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

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
