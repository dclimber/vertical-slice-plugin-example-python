Feature: Student names view slice

  Scenario: Querying student names returns the current student names
    Given command "student.register" succeeds with:
      """
      {
        "name": "Alice",
        "max_courses": 2
      }
      """
    And I remember result field "student_id" as "student_1"
    And command "student.register" succeeds with:
      """
      {
        "name": "Bob",
        "max_courses": 3
      }
      """
    And I remember result field "student_id" as "student_2"
    And command "student.update_name" succeeds with:
      """
      {
        "student_id": "$student_2",
        "name": "Robert"
      }
      """
    Then query "enrollment.student_names" with:
      """
      {
        "student_ids": ["$student_1", "$student_2"]
      }
      """
    And should have field "names" equal to:
      """
      ["Alice", "Robert"]
      """
