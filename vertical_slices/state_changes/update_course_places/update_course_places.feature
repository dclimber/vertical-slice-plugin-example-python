Feature: Update course places slice

  Scenario: Updating a registered course places changes the course summary
    Given command "course.register" succeeds with:
      """
      {
        "name": "Maths",
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_id"
    When command "course.update_places" succeeds with:
      """
      {
        "course_id": "$course_id",
        "places": 5
      }
      """
    Then query "enrollment.course" with:
      """
      {
        "course_id": "$course_id"
      }
      """
    And should have field "places" equal to:
      """
      5
      """
