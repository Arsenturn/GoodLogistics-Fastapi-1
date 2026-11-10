from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from .models import UserStatus


class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    username: str
    email: EmailStr


class UserOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    status: UserStatus
    created_date: datetime


class CurrentUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    status: UserStatus


class CategoryInputSchema(BaseModel):
    category_name: str


class CategoryOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_name: str


class StoreInputSchema(BaseModel):
    store_name: str
    category_id: int
    store_image: Optional[str] = None


class StoreOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    store_name: str
    category_id: int
    store_image: Optional[str] = None


class ProductInputSchema(BaseModel):
    store_id: int
    product_name: str
    price: int = Field(gt=0)
    description: str
    is_original: bool = True


class ProductOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    store_id: int
    product_name: str
    price: int
    description: str
    is_original: bool
    create_date: datetime


class ReviewInputSchema(BaseModel):
    store_id: int
    user_id: int
    text: str
    stars: int = Field(ge=1, le=5)


class ReviewOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    store_id: int
    user_id: int
    text: str
    stars: int
    created_date: datetime



class CityInputSchema(BaseModel):
    city_name: str


class CityOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_name: str



class OrderInputSchema(BaseModel):
    product_id: int
    user_id: int
    city_id: int
    quantity: int = Field(ge=1)


class OrderOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    user_id: int
    city_id: int
    quantity: int
    total_price: int
    created_date: datetime