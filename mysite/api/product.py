from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Product, Store
from mysite.database.schema import ProductInputSchema, ProductOutSchema
from mysite.database.db import SessionLocal

product_router = APIRouter(prefix='/product', tags=['Product'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post('/', response_model=ProductOutSchema)
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    if not db.query(Store).filter(Store.id == product.store_id).first():
        raise HTTPException(detail='Мындай магазин жок', status_code=404)

    product_db = Product(**product.model_dump())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/', response_model=List[ProductOutSchema])
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}/', response_model=ProductOutSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(detail='Мындай продукт жок', status_code=404)
    return product


@product_router.put('/{product_id}/', response_model=dict)
async def update_product(product_id: int, product: ProductInputSchema,
                         db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай продукт жок', status_code=404)

    if not db.query(Store).filter(Store.id == product.store_id).first():
        raise HTTPException(detail='Мындай магазин жок', status_code=404)

    for key, value in product.model_dump().items():
        setattr(product_db, key, value)

    db.commit()
    db.refresh(product_db)
    return {'message': 'Продукт озгорулду'}


@product_router.delete('/{product_id}/', response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай продукт жок', status_code=404)

    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт очту'}