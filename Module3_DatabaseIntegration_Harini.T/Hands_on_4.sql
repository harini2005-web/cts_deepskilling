-- HANDS-ON 4

-- Task 1

-- Question 48

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Question 49

-- Check the EXPLAIN output and identify whether
-- a Full Table Scan is performed on any table.

-- Question 50

-- Record the rows examined and execution plan
-- details from the EXPLAIN output as comments.

-- Task 2

-- Question 51

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

-- Question 52

CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

-- Question 53

CREATE INDEX idx_courses_course_code
ON courses(course_code);

-- Question 54

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Compare this EXPLAIN output with the previous one
-- and document any improvement observed.

-- Question 55

CREATE INDEX idx_enrollments_null_grade
ON enrollments(student_id);

-- MySQL does not support PostgreSQL-style
-- partial indexes with WHERE grade IS NULL.
-- This standard index is the closest equivalent.

