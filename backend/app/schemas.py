from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import TransactionType


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserInDB):
    pass


# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str


# Transaction schemas
class TransactionBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0)
    type: TransactionType
    category: str = Field(..., min_length=1, max_length=50)
    date: Optional[datetime] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[datetime] = None


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    type: TransactionType
    color: str = Field(default="#6366f1", pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: str = Field(default="💰")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[TransactionType] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    is_default: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Pagination
class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    size: int
    pages: int