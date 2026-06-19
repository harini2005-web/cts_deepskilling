# HANDS-ON 6

# Questions 80 - 91

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from models import (
    Department,
    Student,
    Course,
    Enrollment
)

DATABASE_URL = "mysql+mysqlconnector://root:Harini#2005@localhost/college_db_orm"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Session = sessionmaker(bind=engine)
session = Session()

# Question 80

# Session created above.

# Question 81

cs = Department(
    dept_name="Computer Science",
    hod_name="Dr. Ramesh Kumar",
    budget=850000
)

electronics = Department(
    dept_name="Electronics",
    hod_name="Dr. Priya Nair",
    budget=620000
)

mechanical = Department(
    dept_name="Mechanical",
    hod_name="Dr. Suresh Iyer",
    budget=540000
)

session.add_all([
    cs,
    electronics,
    mechanical
])

session.commit()

student1 = Student(
    first_name="Arjun",
    last_name="Mehta",
    email="arjun@college.edu",
    department_id=cs.department_id,
    enrollment_year=2022
)

student2 = Student(
    first_name="Priya",
    last_name="Suresh",
    email="priya@college.edu",
    department_id=cs.department_id,
    enrollment_year=2022
)

student3 = Student(
    first_name="Rohan",
    last_name="Verma",
    email="rohan@college.edu",
    department_id=electronics.department_id,
    enrollment_year=2021
)

student4 = Student(
    first_name="Sneha",
    last_name="Patel",
    email="sneha@college.edu",
    department_id=mechanical.department_id,
    enrollment_year=2023
)

student5 = Student(
    first_name="Vikram",
    last_name="Das",
    email="vikram@college.edu",
    department_id=cs.department_id,
    enrollment_year=2022
)

session.add_all([
    student1,
    student2,
    student3,
    student4,
    student5
])

session.commit()

print("Departments and Students inserted.")

# Question 82

course1 = Course(
    course_name="Data Structures & Algorithms",
    course_code="CS101",
    credits=4,
    department_id=cs.department_id
)

course2 = Course(
    course_name="Database Management Systems",
    course_code="CS102",
    credits=3,
    department_id=cs.department_id
)

course3 = Course(
    course_name="Circuit Theory",
    course_code="EC101",
    credits=3,
    department_id=electronics.department_id
)

session.add_all([
    course1,
    course2,
    course3
])

session.commit()

enrollment1 = Enrollment(
    student_id=student1.student_id,
    course_id=course1.course_id,
    enrollment_date=date.today(),
    grade="A"
)

enrollment2 = Enrollment(
    student_id=student2.student_id,
    course_id=course1.course_id,
    enrollment_date=date.today(),
    grade="B"
)

enrollment3 = Enrollment(
    student_id=student3.student_id,
    course_id=course3.course_id,
    enrollment_date=date.today(),
    grade="A"
)

enrollment4 = Enrollment(
    student_id=student5.student_id,
    course_id=course2.course_id,
    enrollment_date=date.today(),
    grade="B"
)

session.add_all([
    enrollment1,
    enrollment2,
    enrollment3,
    enrollment4
])

session.commit()

print("Courses and Enrollments inserted.")

# Question 83

cs_students = (
    session.query(Student)
    .join(Department)
    .filter(
        Department.dept_name == "Computer Science"
    )
    .all()
)

print("\nStudents in Computer Science Department")

for student in cs_students:
    print(
        student.first_name,
        student.last_name
    )

# Question 84

print("\nEnrollment Details")

enrollments = session.query(
    Enrollment
).all()

for enrollment in enrollments:
    print(
        enrollment.student.first_name,
        enrollment.student.last_name,
        "->",
        enrollment.course.course_name
    )

# Question 85

student = (
    session.query(Student)
    .filter(
        Student.email == "arjun@college.edu"
    )
    .first()
)

if student:
    student.enrollment_year = 2023
    session.commit()
    print("\nStudent updated successfully.")

# Question 86

enrollment = (
    session.query(Enrollment)
    .first()
)

if enrollment:
    session.delete(enrollment)
    session.commit()
    print("\nEnrollment deleted successfully.")

# Question 87

print("\nQuestion 87")
print(
    "Observe the SQL logs generated above "
    "with echo=True."
)
print(
    "Each access to enrollment.student or "
    "enrollment.course may trigger "
    "additional queries."
)

# Question 88

optimized_enrollments = (
    session.query(Enrollment)
    .options(
        joinedload(
            Enrollment.student
        ),
        joinedload(
            Enrollment.course
        )
    )
    .all()
)

# Question 89

print("\nQuestion 89")

for enrollment in optimized_enrollments:
    print(
        enrollment.student.first_name,
        enrollment.student.last_name,
        "->",
        enrollment.course.course_name
    )

print(
    "Check SQL logs. joinedload() should "
    "significantly reduce query count."
)

# Question 90

"""
Before joinedload():

1 query for enrollments
+
N queries for students
+
N queries for courses

Result:
N+1 problem occurs.

After joinedload():

Single JOIN query fetches
enrollments, students and courses.

Query count reduced drastically.
"""

# Question 91

# Django ORM Equivalent

"""
from django.db import models

Enrollment.objects.select_related(
    'student',
    'course'
).all()
"""

session.close()