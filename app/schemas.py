from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# ----------- USER SCHEMAS -----------

class UserBase(BaseModel):
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")  # ✅ Add email here

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="strongpassword123")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")  # ✅ Rename field for clarity
    password: str = Field(..., example="strongpassword123")

class UserOut(UserBase):  # Inherits username and email
    id: int

    class Config:
        orm_mode = True


# ----------- TODO SCHEMAS -----------

class TodoBase(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, Bread, Eggs")
    status: Optional[str] = Field("not_done", example="done")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]

class TodoOut(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# ----------- TOKEN SCHEMAS -----------

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

