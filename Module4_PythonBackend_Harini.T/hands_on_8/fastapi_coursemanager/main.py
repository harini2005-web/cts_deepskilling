from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from database import engine

from models import Base
from models import Course

from schemas import (
    CourseCreate,
    CoursePatch,
    CourseResponse
)

app = FastAPI(
    title="Course API v1",
    version="1.0"
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )


def error_response(
    code,
    message,
    field=None
):
    return {
        "error": {
            "code": code,
            "message": message,
            "field": field
        }
    }


@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    obj = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )

    db.add(obj)

    await db.commit()

    await db.refresh(obj)

    return obj


@app.get(
    "/api/v1/courses/",
    response_model=list[CourseResponse]
)
async def get_courses(
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(Course)

    if search:

        query = query.where(
            Course.name.contains(search)
        )

    query = query.offset(
        (page - 1) * page_size
    ).limit(page_size)

    result = await db.execute(query)

    return result.scalars().all()


@app.get(
    "/api/v1/courses/{id}",
    response_model=CourseResponse
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
            detail=error_response(
                "NOT_FOUND",
                f"Course {id} not found"
            )
        )

    return course


@app.put(
    "/api/v1/courses/{id}",
    response_model=CourseResponse
)
async def replace_course(
    id: int,
    course_data: CourseCreate,
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

    course.name = course_data.name
    course.code = course_data.code
    course.credits = course_data.credits
    course.department_id = \
        course_data.department_id

    await db.commit()

    await db.refresh(course)

    return course


@app.patch(
    "/api/v1/courses/{id}",
    response_model=CourseResponse
)
async def patch_course(
    id: int,
    course_data: CoursePatch,
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
    "/api/v1/courses/{id}",
    status_code=status.HTTP_204_NO_CONTENT
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