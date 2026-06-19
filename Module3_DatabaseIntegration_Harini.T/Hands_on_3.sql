-- HANDS-ON 3

-- Task 1

-- Question 35

SELECT s.student_id,
       s.first_name,
       s.last_name,
       COUNT(e.course_id) AS total_courses
FROM students s
JOIN enrollments e
ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) >
(
    SELECT AVG(course_count)
    FROM
    (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) avg_table
);

-- Question 36

SELECT c.course_name
FROM courses c
WHERE NOT EXISTS
(
    SELECT *
    FROM enrollments e
    WHERE e.course_id = c.course_id
    AND e.grade <> 'A'
);

-- Question 37

SELECT p.professor_id,
       p.prof_name,
       p.department_id,
       p.salary
FROM professors p
WHERE p.salary =
(
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- Question 38

SELECT *
FROM
(
    SELECT d.department_id,
           d.dept_name,
           AVG(p.salary) AS avg_salary
    FROM departments d
    JOIN professors p
    ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) dept_avg
WHERE avg_salary > 85000;

-- Task 2

-- Question 39

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    d.dept_name,
    COUNT(e.course_id) AS total_courses,
    ROUND(
        AVG(
            CASE
                WHEN e.grade = 'A' THEN 4
                WHEN e.grade = 'B' THEN 3
                WHEN e.grade = 'C' THEN 2
                WHEN e.grade = 'D' THEN 1
                WHEN e.grade = 'F' THEN 0
            END
        ),
        2
    ) AS GPA
FROM students s
LEFT JOIN departments d
ON s.department_id = d.department_id
LEFT JOIN enrollments e
ON s.student_id = e.student_id
GROUP BY s.student_id, student_name, d.dept_name;

-- Question 40

CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(
        AVG(
            CASE
                WHEN e.grade = 'A' THEN 4
                WHEN e.grade = 'B' THEN 3
                WHEN e.grade = 'C' THEN 2
                WHEN e.grade = 'D' THEN 1
                WHEN e.grade = 'F' THEN 0
            END
        ),
        2
    ) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Question 41

SELECT *
FROM vw_student_enrollment_summary
WHERE GPA > 3.0;

-- Question 42

UPDATE vw_student_enrollment_summary
SET GPA = 4
WHERE student_id = 1;

-- Multi-table views are generally not updatable
-- because data originates from multiple base tables
-- and the database cannot determine which table
-- should be modified.

-- Question 43

DROP VIEW IF EXISTS vw_course_stats;
DROP VIEW IF EXISTS vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    student_id,
    first_name,
    last_name,
    department_id
FROM students
WHERE enrollment_year >= 2022
WITH CHECK OPTION;

-- Task 3

-- Question 44

DELIMITER $$

CREATE PROCEDURE sp_enroll_student
(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN

    IF EXISTS
    (
        SELECT 1
        FROM enrollments
        WHERE student_id = p_student_id
        AND course_id = p_course_id
    )
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate enrollment not allowed';
    ELSE
        INSERT INTO enrollments
        (
            student_id,
            course_id,
            enrollment_date
        )
        VALUES
        (
            p_student_id,
            p_course_id,
            p_enrollment_date
        );
    END IF;

END$$

DELIMITER ;

-- Question 45

CREATE TABLE department_transfer_log
(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student
(
    IN p_student_id INT,
    IN p_new_department_id INT
)
BEGIN

    DECLARE v_old_department INT;

    START TRANSACTION;

    SELECT department_id
    INTO v_old_department
    FROM students
    WHERE student_id = p_student_id;

    UPDATE students
    SET department_id = p_new_department_id
    WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log
    (
        student_id,
        old_department_id,
        new_department_id
    )
    VALUES
    (
        p_student_id,
        v_old_department,
        p_new_department_id
    );

    COMMIT;

END$$

DELIMITER ;

-- Question 46

START TRANSACTION;

UPDATE students
SET department_id = 999
WHERE student_id = 1;

ROLLBACK;

-- Question 47

START TRANSACTION;

INSERT INTO enrollments
(
    student_id,
    course_id,
    enrollment_date,
    grade
)
VALUES
(
    1,
    3,
    CURDATE(),
    'A'
);

SAVEPOINT first_insert;

INSERT INTO enrollments
(
    student_id,
    course_id,
    enrollment_date,
    grade
)
VALUES
(
    999,
    999,
    CURDATE(),
    'A'
);

ROLLBACK TO first_insert;

COMMIT;