Feature: Student joins course

  Scenario: Student joins a course with available capacity
    Given command "student.register" succeeds with:
      """
      {
        "name": "Max",
        "max_courses": 1
      }
      """
    And I remember result field "student_id" as "student_id"
    And command "course.register" succeeds with:
      """
      {
        "name": "Biology",
        "places": 1
      }
      """
    And I remember result field "course_id" as "course_id"
    When command "enrolment.join_course" succeeds with:
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
