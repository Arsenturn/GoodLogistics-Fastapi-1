from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import Review
from mysite.database.schema import ReviewInputSchema, ReviewOutSchema
from mysite.database.db import SessionLocal

review_router = APIRouter(prefix='/review', tags=['Review'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/', response_model=ReviewOutSchema)
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.model_dump())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.get('/', response_model=List[ReviewOutSchema])
async def list_review(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get('/{review_id}/', response_model=ReviewOutSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(detail='Мындай отзыв жок', status_code=404)
    return review


@review_router.put('/{review_id}/', response_model=dict)
async def update_review(review_id: int, review: ReviewInputSchema,
                        db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail='Мындай отзыв жок', status_code=404)

    for key, value in review.model_dump().items():
        setattr(review_db, key, value)

    db.commit()
    db.refresh(review_db)
    return {'message': 'Отзыв озгорулду'}


@review_router.delete('/{review_id}/', response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail='Мындай отзыв жок', status_code=404)

    db.delete(review_db)
    db.commit()
    return {'message': 'Отзыв очту'}