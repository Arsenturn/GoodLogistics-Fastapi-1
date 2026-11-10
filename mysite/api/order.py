from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Order, Product, User, City
from mysite.database.schema import OrderInputSchema, OrderOutSchema
from mysite.database.db import SessionLocal

order_router = APIRouter(prefix='/order', tags=['Order'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_related(order: OrderInputSchema, db: Session) -> Product:
    """Проверяем, что товар, пользователь и город существуют. Возвращаем товар."""
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(detail='Мындай продукт жок', status_code=404)

    if not db.query(User).filter(User.id == order.user_id).first():
        raise HTTPException(detail='Мындай колдонуучу жок', status_code=404)

    if not db.query(City).filter(City.id == order.city_id).first():
        raise HTTPException(detail='Мындай шаар жок', status_code=404)

    return product


@order_router.post('/', response_model=OrderOutSchema)
async def create_order(order: OrderInputSchema, db: Session = Depends(get_db)):
    product = check_related(order, db)
    order_db = Order(**order.model_dump(), total_price=product.price * order.quantity)
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.get('/', response_model=List[OrderOutSchema])
async def list_order(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get('/{order_id}/', response_model=OrderOutSchema)
async def detail_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(detail='Мындай заказ жок', status_code=404)
    return order


@order_router.put('/{order_id}/', response_model=dict)
async def update_order(order_id: int, order: OrderInputSchema,
                       db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail='Мындай заказ жок', status_code=404)

    product = check_related(order, db)

    for key, value in order.model_dump().items():
        setattr(order_db, key, value)
    order_db.total_price = product.price * order.quantity

    db.commit()
    db.refresh(order_db)
    return {'message': 'Заказ озгорулду'}


@order_router.delete('/{order_id}/', response_model=dict)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail='Мындай заказ жок', status_code=404)

    db.delete(order_db)
    db.commit()
    return {'message': 'Заказ очту'}