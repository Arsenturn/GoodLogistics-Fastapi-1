from .db import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, Enum, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum


class UserStatus(str, PyEnum):
    buyer = 'buyer'
    seller = 'seller'
    manager = 'manager'
    courier = 'courier'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.buyer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user_reviews: Mapped[List['Review']] = relationship(back_populates='user',
                                                        cascade='all, delete-orphan')
    user_orders: Mapped[List['Order']] = relationship(back_populates='user',
                                                      cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user',
                                                            cascade='all, delete-orphan')

    def __str__(self):
        return self.username


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_user: Mapped[User] = relationship(back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(64), unique=True)

    category_stores: Mapped[List['Store']] = relationship(back_populates='category',
                                                          cascade='all, delete-orphan')

    def __str__(self):
        return self.category_name


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    store_name: Mapped[str] = mapped_column(String(64))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(back_populates='category_stores')
    store_image: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    store_products: Mapped[List['Product']] = relationship(back_populates='store',
                                                           cascade='all, delete-orphan')
    store_reviews: Mapped[List['Review']] = relationship(back_populates='store',
                                                         cascade='all, delete-orphan')

    def __str__(self):
        return self.store_name


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped[Store] = relationship(back_populates='store_products')
    product_name: Mapped[str] = mapped_column(String(128))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    is_original: Mapped[bool] = mapped_column(Boolean, default=True)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    product_orders: Mapped[List['Order']] = relationship(back_populates='product')

    def __str__(self):
        return self.product_name


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped[Store] = relationship(back_populates='store_reviews')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(back_populates='user_reviews')
    text: Mapped[str] = mapped_column(Text)
    stars: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __str__(self):
        return f'{self.user}, {self.store}, {self.stars}'


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    city_name: Mapped[str] = mapped_column(String(64), unique=True)

    city_orders: Mapped[List['Order']] = relationship(back_populates='city')

    def __str__(self):
        return self.city_name


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(back_populates='product_orders')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(back_populates='user_orders')
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship(back_populates='city_orders')
    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __str__(self):
        return f'{self.user}, {self.product}, {self.quantity}'