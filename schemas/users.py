# app/schemas/users.py
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    username: EmailStr = Field(..., example="admin@example.com")
    password: str      = Field(..., min_length=6, example="supersecret")

class UserLogin(BaseModel):
    username: EmailStr = Field(..., example="admin@example.com")
    password: str      = Field(..., min_length=6, example="supersecret")
