from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Department(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    head_of_dept = db.Column(
        db.String(100)
    )

    budget = db.Column(
        db.Float
    )

    courses = db.relationship(
        'Course',
        back_populates='department'
    )

    students = db.relationship(
        'Student',
        back_populates='department'
    )


class Course(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    code = db.Column(
        db.String(20),
        unique=True
    )

    credits = db.Column(
        db.Integer
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey('department.id')
    )

    department = db.relationship(
        'Department',
        back_populates='courses'
    )

    enrollments = db.relationship(
        'Enrollment',
        back_populates='course'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits
        }


class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(100)
    )

    last_name = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(100)
    )

    enrollment_year = db.Column(
        db.Integer
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey('department.id')
    )

    department = db.relationship(
        'Department',
        back_populates='students'
    )

    enrollments = db.relationship(
        'Enrollment',
        back_populates='student'
    )


class Enrollment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id')
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('course.id')
    )

    grade = db.Column(
        db.String(10)
    )

    student = db.relationship(
        'Student',
        back_populates='enrollments'
    )

    course = db.relationship(
        'Course',
        back_populates='enrollments'
    )