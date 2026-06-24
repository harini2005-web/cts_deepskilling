from django.db.models import Count, F
from .models import Department, Course, Student


# Create Departments
cs = Department.objects.create(
    name="Computer Science",
    head_of_dept="Dr. Smith",
    budget=500000
)

ece = Department.objects.create(
    name="Electronics",
    head_of_dept="Dr. John",
    budget=400000
)

# Create Courses
Course.objects.create(
    name="Python Programming",
    code="CS101",
    credits=4,
    department=cs
)

Course.objects.create(
    name="Database Systems",
    code="CS102",
    credits=3,
    department=cs
)

Course.objects.create(
    name="Digital Electronics",
    code="EC101",
    credits=4,
    department=ece
)

Course.objects.create(
    name="Microprocessors",
    code="EC102",
    credits=3,
    department=ece
)

# Create Students
Student.objects.create(
    first_name="Harini",
    last_name="T",
    email="harini1@example.com",
    department=cs,
    enrollment_year=2024
)

Student.objects.create(
    first_name="Asha",
    last_name="K",
    email="asha@example.com",
    department=cs,
    enrollment_year=2024
)

Student.objects.create(
    first_name="Ravi",
    last_name="M",
    email="ravi@example.com",
    department=ece,
    enrollment_year=2023
)

Student.objects.create(
    first_name="Priya",
    last_name="S",
    email="priya@example.com",
    department=ece,
    enrollment_year=2023
)

Student.objects.create(
    first_name="Kumar",
    last_name="R",
    email="kumar@example.com",
    department=cs,
    enrollment_year=2022
)

# Query courses by department
courses = Course.objects.filter(
    department__name="Computer Science"
)

# Count courses per department
departments = Department.objects.annotate(
    course_count=Count('course')
)

# Fetch students with department
students = Student.objects.select_related(
    'department'
)

# Increase budget by 10%
Department.objects.update(
    budget=F('budget') * 1.1
)