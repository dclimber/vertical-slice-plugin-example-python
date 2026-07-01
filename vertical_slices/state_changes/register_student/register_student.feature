Feature: Register student slice

  Scenario: Registering a student records the student details
    Given command "student.register" succeeds with:
      """
      {
        "name": "Alice",
        "max_courses": 3
      }
      """
    And I remember result field "student_id" as "student_id"
    Then query "enrollment.student" with:
      """
      {
        "student_id": "$student_id"
      }
      """
    And should have field "name" equal to:
      """
      "Alice"
      """
    And should have field "max_courses" equal to:
      """
      3
      """
    And should have field "course_ids" equal to:
      """
      []
      """
