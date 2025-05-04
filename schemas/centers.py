# schemas/centers.py

from pydantic import BaseModel, Field

class CenterBase(BaseModel):
    center: str = Field(..., example="Centro A")
    phonenumber: str = Field(..., example="+34123456789")

class CenterCreate(CenterBase):
    pass

class CenterUpdate(CenterBase):
    pass

class CenterRead(CenterBase):
    id: int

    class Config:
        orm_mode = True
