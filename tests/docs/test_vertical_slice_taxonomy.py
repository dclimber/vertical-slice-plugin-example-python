from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_docs_describe_domain_area_import_shims() -> None:
    readme = (ROOT / "README.md").read_text()
    architecture = (ROOT / "plugin-architecture.md").read_text()

    assert "domain-area import shims" in readme
    assert "Domain-area import shims" in architecture
    assert "vertical slice packages" not in architecture
    assert "package-level vertical slices" not in architecture


def test_docs_describe_bdd_features_as_flow_or_use_case_specs() -> None:
    readme = (ROOT / "README.md").read_text()
    architecture = (ROOT / "plugin-architecture.md").read_text()

    assert "flow specifications" in readme
    assert "flow/use-case specifications" in architecture


def test_docs_describe_the_public_package_taxonomy() -> None:
    readme = (ROOT / "README.md").read_text()
    architecture = (ROOT / "plugin-architecture.md").read_text()

    for folder in (
        "vertical_slices/courses_events",
        "vertical_slices/enrollment_events",
        "vertical_slices/student_events",
        "vertical_slices/automations",
        "vertical_slices/state-changes",
        "vertical_slices/state-views",
    ):
        assert folder in readme
        assert folder in architecture

    assert "shared contracts" in readme
    assert "shared contracts" in architecture
    assert "command -> event slices" in readme
    assert "command -> event slices" in architecture
    assert "event -> query/read-model slices" in readme
    assert "event -> query/read-model slices" in architecture
    assert "event -> read model -> command -> event" in readme
    assert "event -> read model -> automatic process ->" in architecture


def test_docs_do_not_present_broad_domain_packages_as_the_final_shape() -> None:
    readme = (ROOT / "README.md").read_text()
    architecture = (ROOT / "plugin-architecture.md").read_text()

    forbidden_phrases = (
        "vertical_slices/student_slice",
        "vertical_slices/course_slice",
        "vertical_slices/enrolment_slice",
    )

    for phrase in forbidden_phrases:
        assert phrase not in readme
        assert phrase not in architecture


def test_docs_do_not_reference_removed_example_modules() -> None:
    readme = (ROOT / "README.md").read_text()
    architecture = (ROOT / "plugin-architecture.md").read_text()

    for phrase in (
        "dcb_enrolment_with_vertical_slices",
        "EnrolmentWithVerticalSlices",
        "src/examples",
    ):
        assert phrase not in readme
        assert phrase not in architecture
