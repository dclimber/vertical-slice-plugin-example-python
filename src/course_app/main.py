from __future__ import annotations

from collections.abc import Mapping

from course_app.app import CourseApp
from course_app.use_cases import register_use_cases


def create_app(env: Mapping[str, str] | None = None) -> CourseApp:
    app = CourseApp(env=env)
    register_use_cases(app)
    return app
