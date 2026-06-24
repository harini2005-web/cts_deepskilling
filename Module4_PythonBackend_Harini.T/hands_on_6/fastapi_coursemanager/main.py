from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    version="1.0"
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )


@app.get("/")
async def root():

    return {
        "message": "API running"
    }


@app.post(
    "/api/courses/",
    response_model=CourseResponse
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
    "/api/courses/{course_id}",
    response_model=CourseResponse
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@app.get(
    "/api/courses/",
    response_model=list[CourseResponse]
)
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(Course)

    if department_id is not None:
        query = query.where(
            Course.department_id ==
            department_id
        )

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


@app.put(
    "/api/courses/{course_id}",
    response_model=CourseResponse
)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
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
    "/api/courses/{course_id}"
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
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

    return {
        "message": "deleted"
    }