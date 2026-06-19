-- HANDS-ON 1

-- Task 1

-- Question 1
CREATE DATABASE college_db;

USE college_db;

-- Question 2
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT
);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2)
);

CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2)
);

-- Question 3
-- NOT NULL, UNIQUE and PRIMARY KEY constraints added above.

-- Question 4
ALTER TABLE students
ADD CONSTRAINT fk_student_department
FOREIGN KEY (department_id)
REFERENCES departments(department_id);

ALTER TABLE courses
ADD CONSTRAINT fk_course_department
FOREIGN KEY (department_id)
REFERENCES departments(department_id);

ALTER TABLE enrollments
ADD CONSTRAINT fk_enrollment_student
FOREIGN KEY (student_id)
REFERENCES students(student_id);

ALTER TABLE enrollments
ADD CONSTRAINT fk_enrollment_course
FOREIGN KEY (course_id)
REFERENCES courses(course_id);

ALTER TABLE professors
ADD CONSTRAINT fk_professor_department
FOREIGN KEY (department_id)
REFERENCES departments(department_id);

-- Question 5
SHOW TABLES;

DESCRIBE departments;
DESCRIBE students;
DESCRIBE courses;
DESCRIBE enrollments;
DESCRIBE professors;

-- Task 2

-- Question 6
-- 1NF Analysis:
-- Every column stores atomic values.
-- Example violation: multiple phone numbers in a single column.

-- Question 7
-- 2NF Analysis:
-- Every non-key attribute depends on the entire key.
-- No partial dependencies.

-- Question 8
-- 3NF Analysis:
-- No transitive dependencies.
-- Storing dept_name in students would violate 3NF.

-- Question 9
-- Enrollments table satisfies 3NF because all non-key
-- attributes depend directly on the key.

-- Task 3

-- Question 10
ALTER TABLE students
ADD phone_number VARCHAR(15);

-- Question 11
ALTER TABLE courses
ADD max_seats INT DEFAULT 60;

-- Question 12
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (
    grade IN ('A','B','C','D','F')
    OR grade IS NULL
);

-- Question 13
ALTER TABLE departments
RENAME COLUMN hod_name TO head_of_dept;

-- Question 14
ALTER TABLE students
DROP COLUMN phone_number;