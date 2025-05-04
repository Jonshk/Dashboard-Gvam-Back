from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    username: EmailStr = Field(..., example="usuario@ejemplo.com")
    password: str     = Field(..., min_length=6, example="Contraseña123")

class UserLogin(BaseModel):
    username: EmailStr = Field(..., example="usuario@ejemplo.com")
    password: str      = Field(..., min_length=6, example="Contraseña123")
