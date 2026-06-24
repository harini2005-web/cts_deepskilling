from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    BackgroundTasks
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from database import engine

from models import Base
from models import Course

from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse
)

app = FastAPI(
    title="Course Management API",
    description="Hands On 7 FastAPI CRUD",
    version="1.0",
    contact={
        "name": "Harini"
    }
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )


def send_confirmation_email(
    student_email: str
):

    print(
        f"Sending confirmation to {student_email}"
    )


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create Course",
    response_description="Created Course"
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    new_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    return new_course


@app.get(
    "/api/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)
async def get_courses(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course)
    )

    return result.scalars().all()


@app.get(
    "/api/courses/{id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_course(
    id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == id
        )
    )

    course = result.scalar_one_or_none()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@app.put(
    "/api/courses/{id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == id
        )
    )

    course = result.scalar_one_or_none()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    for key, value in \
        course_data.dict(
            exclude_unset=True
        ).items():

        setattr(
            course,
            key,
            value
        )

    await db.commit()

    await db.refresh(course)

    return course


@app.delete(
    "/api/courses/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == id
        )
    )

    course = result.scalar_one_or_none()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    await db.delete(course)

    await db.commit()


@app.post(
    "/api/enrollments/",
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        send_confirmation_email,
        "student@email.com"
    )

    return {
        "message":
        "Enrollment created"
    }


@app.get(
    "/api/courses/{id}/students/",
    tags=["Courses"]
)
async def get_students(
    id: int
):

    return {
        "course_id": id,
        "students": []
    }