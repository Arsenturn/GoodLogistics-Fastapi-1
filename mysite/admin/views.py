from sqladmin import ModelView
from mysite.database.models import User, Category, Store, Product, Review, City, Order


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.status,
        User.created_date,
    ]


class CategoryAdmin(ModelView, model=Category):
    column_list = [
        Category.id,
        Category.category_name,
    ]


class StoreAdmin(ModelView, model=Store):
    column_list = [
        Store.id,
        Store.store_name,
        Store.category_id,
        Store.store_image,
    ]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.store_id,
        Product.product_name,
        Product.price,
        Product.is_original,
        Product.create_date,
    ]


class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.id,
        Review.store_id,
        Review.user_id,
        Review.stars,
        Review.text,
    ]


class CityAdmin(ModelView, model=City):
    column_list = [
        City.id,
        City.city_name,
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.product_id,
        Order.user_id,
        Order.city_id,
        Order.quantity,
        Order.total_price,]