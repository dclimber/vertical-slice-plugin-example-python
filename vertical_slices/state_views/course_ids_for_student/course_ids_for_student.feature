Feature: Course IDs for student view slice

  Scenario: Querying course IDs for a student returns current joined courses
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
    And I remember result field "course_id" as "course_1"
    And command "course.register" succeeds with:
      """
      {
        "name": "Physics",
        "places": 2
      }
      """
    And I remember result field "course_id" as "course_2"
    And command "enrollment.join_course" succeeds with:
      """
      {
        "student_id": "$student_id",
        "course_id": "$course_1"
      }
      """
    And command "enrollment.join_course" succeeds with:
      """
      {
        "student_id": "$student_id",
        "course_id": "$course_2"
      }
      """
    Then query "enrollment.course_ids_for_student" with:
      """
      {
        "student_id": "$student_id"
      }
      """
    And should have field "course_ids" equal to:
      """
      ["$course_1", "$course_2"]
      """
