Feature: Update student name slice

  Scenario: Updating a registered student's name changes the student summary
    Given command "student.register" succeeds with:
      """
      {
        "name": "Alice",
        "max_courses": 3
      }
      """
    And I remember result field "student_id" as "student_id"
    When command "student.update_name" succeeds with:
      """
      {
        "student_id": "$student_id",
        "name": "Ada"
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
