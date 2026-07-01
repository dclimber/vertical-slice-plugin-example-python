Feature: Course names view slice

  Scenario: Querying course names returns the current course names
    Given command "course.register" succeeds with:
      """
      {
        "name": "Maths",
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_1"
    And command "course.register" succeeds with:
      """
      {
        "name": "Science",
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_2"
    And command "course.update_name" succeeds with:
      """
      {
        "course_id": "$course_2",
        "name": "Physics"
      }
      """
    Then query "enrollment.course_names" with:
      """
      {
        "course_ids": ["$course_1", "$course_2"]
      }
      """
    And should have field "names" equal to:
      """
      ["Maths", "Physics"]
      """
