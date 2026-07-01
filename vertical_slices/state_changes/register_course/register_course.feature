Feature: Register course slice

  Scenario: Registering a course records the course details
    Given command "course.register" succeeds with:
      """
      {
        "name": "Maths",
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_id"
    Then query "enrollment.course" with:
      """
      {
        "course_id": "$course_id"
      }
      """
    And should have field "name" equal to:
      """
      "Maths"
      """
    And should have field "places" equal to:
      """
      2
      """
    And should have field "student_ids" equal to:
      """
      []
      """
