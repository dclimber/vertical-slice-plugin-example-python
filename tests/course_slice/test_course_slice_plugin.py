from __future__ import annotations

from dataclasses import dataclass, field

from course_slice.events import CourseNameUpdated, CoursePlacesUpdated, CourseRegistered
from course_slice.plugin import course_slice

@dataclass
class RecordingRegistry:
    events: dict[str, type] = field(default_factory=dict)
    event_versions: dict[str, int] = field(default_factory=dict)

    def event(self, name: str, event_type: type, version: int) -> None:
        self.events[name] = event_type
        self.event_versions[name] = version


def test_course_slice_plugin_registers_events() -> None:
    registry = RecordingRegistry()

    course_slice.register(registry)

    assert registry.events == {
        "course.registered": CourseRegistered,
        "course.name_updated": CourseNameUpdated,
        "course.places_updated": CoursePlacesUpdated,
    }
    assert registry.event_versions == {
        "course.registered": 1,
        "course.name_updated": 1,
        "course.places_updated": 1,
    }
