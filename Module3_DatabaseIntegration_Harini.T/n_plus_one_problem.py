# HANDS-ON 4
# Task 3
# N+1 Problem Demonstration

import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harini#2005",
    database="college_db"
)

cursor = conn.cursor(dictionary=True)

# Question 56

start_time = time.time()

cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()

query_count = 1

for enrollment in enrollments:
    cursor.execute(
        """
        SELECT first_name, last_name
        FROM students
        WHERE student_id = %s
        """,
        (enrollment["student_id"],)
    )

    student = cursor.fetchone()

    print(
        f"Enrollment ID: {enrollment['enrollment_id']} | "
        f"Student: {student['first_name']} {student['last_name']}"
    )

    query_count += 1

end_time = time.time()

print("\nQuestion 56")
print("N+1 Queries Executed:", query_count)
print("Execution Time:", end_time - start_time, "seconds")


# Question 57

start_time = time.time()

cursor.execute("""
SELECT
    e.enrollment_id,
    s.first_name,
    s.last_name,
    c.course_name,
    e.grade
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id
""")

records = cursor.fetchall()

for record in records:
    print(
        f"Enrollment ID: {record['enrollment_id']} | "
        f"Student: {record['first_name']} {record['last_name']} | "
        f"Course: {record['course_name']} | "
        f"Grade: {record['grade']}"
    )

end_time = time.time()

print("\nQuestion 57")
print("Queries Executed: 1")
print("Execution Time:", end_time - start_time, "seconds")


# Question 58

print("\nQuestion 58")
print("Comparison Complete")
print("N+1 Approach -> Multiple Database Round Trips")
print("JOIN Approach -> Single Database Round Trip")


# Question 59

print("\nQuestion 59")
print("For 10,000 enrollments:")
print("N+1 Approach = 10,001 Queries")
print("JOIN Approach = 1 Query")

cursor.close()
conn.close()