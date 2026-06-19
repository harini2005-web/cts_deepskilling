#HANDS_ON_6


# Question 75

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    Boolean
)

from sqlalchemy.orm import (
    declarative_base,
    relationship
)

# Question 76

DATABASE_URL = "mysql+mysqlconnector://root:your_password@localhost/college_db_orm"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base = declarative_base()

# Question 77

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    department_name = Column(
        String(100),
        nullable=False
    )

    budget = Column(Float)

    students = relationship(
        "Student",
        back_populates="department"
    )

    professors = relationship(
        "Professor",
        back_populates="department"
    )

    courses = relationship(
        "Course",
        back_populates="department"
    )


# Question 77

class Student(Base):
    __tablename__ = "students"

    student_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = Column(String(50))
    last_name = Column(String(50))

    email = Column(
        String(100),
        unique=True
    )

    enrollment_year = Column(Integer)

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="students"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )

    # Question 98 (Hands-On 7)
    is_active = Column(
        Boolean,
        default=True
    )


# Question 77

class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = Column(String(50))
    last_name = Column(String(50))

    salary = Column(Float)

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="professors"
    )


# Question 77

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    course_code = Column(
        String(20),
        unique=True
    )

    course_name = Column(String(100))

    credits = Column(Integer)

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="courses"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )

    schedules = relationship(
        "CourseSchedule",
        back_populates="course"
    )


# Question 77

class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.student_id")
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.course_id")
    )

    enrollment_date = Column(Date)

    grade = Column(String(2))

    student = relationship(
        "Student",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )


# Question 102 (Hands-On 7)

class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.course_id")
    )

    day_of_week = Column(String(20))

    start_time = Column(String(20))

    end_time = Column(String(20))

    course = relationship(
        "Course",
        back_populates="schedules"
    )


# Question 78

# Relationships are implemented using:
# relationship()
# back_populates
# ForeignKey()


# Question 79

Base.metadata.create_all(engine)

print("All tables created successfully.")