# Student Enrollment as Composable Vertical Slices

Short version:

- Student enrollment is a small problem that exposes a big architecture issue.
- A student has a course limit.
- A course has a seat limit.
- Joining a course must check both facts at the same time.
- That is the classic Dynamic Consistency Boundary problem.
- Event Modeling gives us small vertical slices.
- Python packages give those slices clean code boundaries.
- Domain events are the contracts.
- The event store is the communication path.
- Plugins compose the business app.

This article uses a spiral structure:

- first pass: understand the story;
- second pass: understand the architecture;
- third pass: understand how to add and remove behavior.

## First Spiral: The Story

### 1. The CRUD World

The ordinary model is tempting:

- `Student`
- `Course`
- `Enrollment`
- a service that mutates tables
- a transaction around everything

It works until the rules become real.

### 2. Call to use Event Sourcing

The use case:

- register a student
- register a course
- let the student join the course
- list students for the course

The hidden business rules:

- the student must exist
- the course must exist
- the course must have a free seat
- the student must not exceed their course limit
- the student must not already be on that course

### 3. Refusal of the Call for Event Sourcing

The usual objection:

- "Just put it in one aggregate."
- "Just lock the course."
- "Just lock the student."
- "Just use a relational transaction."

But the decision needs facts from two timelines:

- events tagged with the student
- events tagged with the course

That boundary is not static. It is chosen by the decision.

### 4. Meeting the Alternative

Dynamic Consistency Boundaries say:

- do not model one permanent aggregate boundary too early
- for each decision, select the event streams needed for that decision
- enforce the rule over that selected history
- append the new event if the facts still hold

For `join_course`, the selected history is:

- student registration and student course-limit changes
- course registration and course capacity changes
- previous joins and leaves for the same student
- previous joins and leaves for the same course

### Please ask yourself a question:

What is the smallest history that makes `student joins course` safe?

__*Answers are at the end of the article__.

---

## Second Spiral: The Architecture

### 5. Crossing the Threshold into the "Scary world of Event Sourcing"

Event Modeling gives us the vertical slices:

- state-change: `command -> event`
- state-view: `event -> query/read model`
- automation: `event -> view -> automatic trigger -> command -> event`

Each slice is autonomous.

Autonomous means:

- it has one job
- it can be tested alone
- it registers its public command, query, or automation
- it communicates through durable events, not private calls

### 6. Tests, Allies, Enemies

Clean Architecture gives the pressure:

- business rules should not be trapped inside frameworks
- use cases should be testable without UI or database details
- source code dependencies should point toward policy, not tooling

In Python, the practical move is boring and effective:

- make each slice a Python package
- give each package a `pyproject.toml`
- expose a small plugin object
- keep the app composition in `src/course_app`

This repo does that:

- composition contracts live in `kernel/course_kernel`
- event contracts live in `vertical_slices/*_events`
- state changes live in `vertical_slices/state_changes/*`
- state views live in `vertical_slices/state_views/*`
- future automations live in `vertical_slices/automations/*`
- the app composes them in `src/course_app/use_cases.py`

### 7. Coming closer to a solution

Domain events are the contract between slices.

Examples:

- `StudentRegistered`
- `StudentMaxCoursesUpdated`
- `CourseRegistered`
- `CoursePlacesUpdated`
- `StudentJoinedCourse`
- `StudentLeftCourse`

The contract is not "call my class".

The contract is:

- this event happened
- these fields exist
- these tags identify where it belongs
- future slices may consume it

### 8. The Ordeal

`join_course` is the hard part.

It is not hard because the code is large.

It is hard because it crosses natural ownership lines:

- student facts
- course facts
- enrollment facts

The slice solves this by reading the selected boundary, then deciding:

- course exists?
- student exists?
- course has capacity?
- student has capacity?
- duplicate enrollment?

If yes, append `StudentJoinedCourse`.

Communication happens through the event store:

- command slices append events
- view slices read events
- automations will observe views and emit commands
- use cases compose command/query names, not object graphs

### Action question:

If a new slice cannot call another slice directly, what must it publish or read?

__*Answers are at the end of the article__.

---

## Third Spiral: Composing the Business App

### 9. An approach

A potential approach is a plugin-shaped business system.

Inspired by `pytest`:

- slices are packages
- each package exposes a plugin
- the app has a registry
- plugins register commands, queries, events, or automations
- the composition root decides which plugins are active

To add a slice:

- write the slice package
- add it to the main `pyproject.toml`
- register its plugin in the app
- add it to the relevant use case
- add or update the Gherkin flow
- add the `pytest-bdd` scenario test

That is how we compose business apps here.

### 10. Spec-driven development

End-to-end behavior is specified as Gherkin:

- the source of truth is the `.feature` file
- `pytest-bdd` binds it to executable tests
- the test verifies the composed app, not just one package

Example flow:

- `docs/features/enrolment/student_joins_course.feature`
- `tests/bdd/test_enrolment_flows.py`

The Gherkin tells the business story.

The pytest-bdd test proves the app still tells that story.

### 11. App maintenance

Removing a slice should be a normal operation, not surgery.

If a slice is not needed:

- delete it from the main `pyproject.toml`
- de-register the plugin from the app
- remove it from the use-case composition
- update the Gherkin end-to-end spec
- update the corresponding `pytest-bdd` test
- then delete the slice package

The order matters.

First remove it from the composition.

Then prove the remaining app still has a true story.

Then delete the code.

### 12. A potential solution?

The architecture in one line:

> Business apps are composed from autonomous event-modeled Python packages, with
> domain events as contracts and the event store as the integration mechanism.

The practical rule:

- state-change slices decide and emit events
- state-view slices answer questions from events
- automation slices turn observed state into commands
- Gherkin validates full flows
- plugin registration controls what the app is

Action question:

Which business capability in your system could be removed by changing
composition first and deleting code second?

## References

- Event Modeling: commands, events, views, automation, and slices:
  <https://eventmodeling.org/posts/event-modeling-cheatsheet/>
- Event Modeling overview and workflow-step contracts:
  <https://eventmodeling.org/posts/what-is-event-modeling/>
- Clean Architecture dependency direction and testability:
  <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- Hero's Journey / monomyth background:
  <https://en.wikipedia.org/wiki/Hero%27s_journey>

## Appendix: Suggested Answers

### Answer 1

The smallest safe history for `student joins course` is the history needed to
prove both sides of the rule:

- for the student: registered, max-course changes, joined courses, left courses
- for the course: registered, place changes, joined students, left students

That is the dynamic consistency boundary for this decision.

### Answer 2

If slices cannot call each other directly, they must communicate through durable
contracts:

- publish domain events
- read domain events
- expose commands or queries through registration
- let the event store carry facts between slices

### Answer 3

A removable capability is one where the composition names the dependency
explicitly:

- package path in `pyproject.toml`
- plugin registration in the app
- command/query name in a use case
- Gherkin scenario proving the end-to-end behavior

If those places are explicit, removal is mostly composition work before it is
deletion work.
