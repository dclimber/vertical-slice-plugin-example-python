Feature: Student summary view slice

  Scenario: Querying a student summary returns the current student state
    Given command "student.register" succeeds with:
      """
      {
        "name": "Alice",
        "max_courses": 1
      }
      """
    And I remember result field "student_id" as "student_id"
    And command "course.register" succeeds with:
      """
      {
        "name": "Maths",
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_id"
    And command "student.update_name" succeeds with:
      """
      {
        "student_id": "$student_id",
        "name": "Ada"
      }
      """
    And command "student.update_max_courses" succeeds with:
      """
      {
        "student_id": "$student_id",
        "max_courses": 3
      }
      """
    And command "enrollment.join_course" succeeds with:
      """
      {
        "student_id": "$student_id",
        "course_id": "$course_id"
      }
      """
    Then query "enrollment.student" with:
      """
      {
        "student_id": "$student_id"
      }
      """
    And should have field "name" equal to:
      """
      "Ada"
      """
    And should have field "max_courses" equal to:
      """
      3
      """
    And should have field "course_ids" equal to:
      """
      ["$course_id"]
      """
