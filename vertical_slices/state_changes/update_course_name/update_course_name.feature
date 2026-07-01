Feature: Update course name slice

  Scenario: Updating a registered course name changes the course summary
    Given command "course.register" succeeds with:
      """
      {
        "name": "Maths",
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_id"
    When command "course.update_name" succeeds with:
      """
      {
        "course_id": "$course_id",
        "name": "Physics"
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
