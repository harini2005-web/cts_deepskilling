from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String,
        unique=True
    )

    hashed_password = Column(
        String
    )

    is_active = Column(
        Boolean,
        default=True
    )