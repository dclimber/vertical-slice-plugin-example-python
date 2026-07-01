Feature: Update student max courses slice

  Scenario: Updating a registered student's course limit changes the student summary
    Given command "student.register" succeeds with:
      """
      {
        "name": "Alice",
        "max_courses": 3
      }
      """
    And I remember result field "student_id" as "student_id"
    When command "student.update_max_courses" succeeds with:
      """
      {
        "student_id": "$student_id",
        "max_courses": 5
      }
      """
    Then query "enrollment.student" with:
      """
      {
        "student_id": "$student_id"
      }
      """
    And should have field "max_courses" equal to:
      """
      5
      """
