from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=128)


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[A-Za-z0-9_.-]+$",
    )
    password: str = Field(min_length=8, max_length=128)


class PersonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    gender: Literal["Male", "Female"]
    age: int = Field(ge=0, le=150)


class PersonUpdate(PersonCreate):
    pass


class PersonResponse(PersonCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PersonList(BaseModel):
    items: list[PersonResponse]
    total: int
