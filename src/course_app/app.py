from __future__ import annotations

from collections.abc import Mapping

from eventsourcing.dcb.application import DCBApplication
from eventsourcing.dcb.msgpack import MessagePackMapper
from eventsourcing.utils import get_topic

from course_app.kernel.composition import Composition


class CourseApp(DCBApplication):
    env: Mapping[str, str] = {
        "MAPPER_TOPIC": get_topic(MessagePackMapper),
        **DCBApplication.env,
    }

    def __init__(self, env: Mapping[str, str] | None = None) -> None:
        super().__init__(env)
        self.composition = Composition()

    def handle_command(self, name: str, /, **kwargs: object) -> object:
        slice_factory = self.composition.registry.commands[name]
        return self.do(slice_factory(**kwargs))

    def handle_query(self, name: str, /, **kwargs: object) -> object:
        slice_factory = self.composition.registry.queries[name]
        return self.do(slice_factory(**kwargs))
