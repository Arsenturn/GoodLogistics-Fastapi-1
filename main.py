from fastapi import FastAPI
import uvicorn
from mysite.admin.setup import setup_admin
from mysite.api import auth, category, city, order, product, review, store, user

logistics_app = FastAPI(title='GoodsLogistics')
logistics_app.include_router(auth.auth_router)
logistics_app.include_router(user.user_router)
logistics_app.include_router(category.category_router)
logistics_app.include_router(store.store_router)
logistics_app.include_router(product.product_router)
logistics_app.include_router(review.review_router)
logistics_app.include_router(city.city_router)
logistics_app.include_router(order.order_router)

setup_admin(logistics_app)


if __name__ == '__main__':
    uvicorn.run(logistics_app, host='127.0.0.1', port=8000)