Feature: Student IDs for course view slice

  Scenario: Querying student IDs for a course returns current enrolled students
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
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_id"
    And command "enrollment.join_course" succeeds with:
      """
      {
        "student_id": "$student_id",
        "course_id": "$course_id"
      }
      """
    Then query "enrollment.student_ids_for_course" with:
      """
      {
        "course_id": "$course_id"
      }
      """
    And should have field "student_ids" equal to:
      """
      ["$student_id"]
      """
