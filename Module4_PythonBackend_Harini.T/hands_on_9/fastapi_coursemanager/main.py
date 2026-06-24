from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from jose import jwt
from jose import JWTError

from passlib.context import CryptContext

from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from database import (
    get_db,
    engine
)

from models import (
    Base,
    User
)

from schemas import (
    UserRegister,
    UserLogin,
    Token
)

SECRET_KEY = "secretkey123"

ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login"
)

app = FastAPI(
    title="Secure Course API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )


def get_password_hash(
    password: str
):

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    data: dict
):

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


async def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get(
            "sub"
        )

        return email

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


@app.post(
    "/api/v1/auth/register"
)
async def register(
    user: UserRegister,
    db: AsyncSession = Depends(
        get_db
    )
):

    result = await db.execute(
        select(User).where(
            User.email ==
            user.email
        )
    )

    existing_user = \
        result.scalar_one_or_none()

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email exists"
        )

    new_user = User(
        email=user.email,
        hashed_password=
        get_password_hash(
            user.password
        )
    )

    db.add(new_user)

    await db.commit()

    return {
        "message":
        "Registered"
    }


@app.post(
    "/api/v1/auth/login",
    response_model=Token
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(
        get_db
    )
):

    result = await db.execute(
        select(User).where(
            User.email ==
            user.email
        )
    )

    db_user = \
        result.scalar_one_or_none()

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub":
            db_user.email
        }
    )

    return {
        "access_token":
        token,
        "token_type":
        "bearer"
    }


@app.get(
    "/api/v1/courses/"
)
async def get_courses():

    return [
        {
            "id": 1,
            "name": "Python"
        }
    ]


@app.post(
    "/api/v1/courses/"
)
async def create_course(
    current_user:
    str = Depends(
        get_current_user
    )
):

    return {
        "message":
        "course created",
        "user":
        current_user
    }


@app.delete(
    "/api/v1/courses/{id}"
)
async def delete_course(
    id: int,
    current_user:
    str = Depends(
        get_current_user
    )
):

    return {
        "deleted": id
    }


"""
OAuth2 Authorization Code Flow:

1. User logs in through an
   authorization server.

2. Server returns an
   authorization code.

3. Client exchanges the code
   for an access token.

In this hands-on we use a
simpler JWT flow where login
returns a token directly.
"""