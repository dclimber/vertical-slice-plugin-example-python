Feature: Course summary view slice

  Scenario: Querying a course summary returns the current course state
    Given command "student.register" succeeds with:
      """
      {
        "name": "Alice",
        "max_courses": 2
      }
      """
    And I remember result field "student_id" as "student_id"
    And command "course.register" succeeds with:
      """
      {
        "name": "Maths",
        "places": 1
      }
      """
    And I remember result field "course_id" as "course_id"
    And command "course.update_name" succeeds with:
      """
      {
        "course_id": "$course_id",
        "name": "Physics"
      }
      """
    And command "course.update_places" succeeds with:
      """
      {
        "course_id": "$course_id",
        "places": 3
      }
      """
    And command "enrollment.join_course" succeeds with:
      """
      {
        "student_id": "$student_id",
        "course_id": "$course_id"
      }
      """
    Then query "enrollment.course" with:
      """
      {
        "course_id": "$course_id"
      }
      """
    And should have field "name" equal to:
      """
      "Physics"
      """
    And should have field "places" equal to:
      """
      3
      """
    And should have field "student_ids" equal to:
      """
      ["$student_id"]
      """
