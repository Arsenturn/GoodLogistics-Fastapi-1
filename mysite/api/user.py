from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import User
from mysite.database.schema import UserUpdateSchema, UserOutputSchema
from mysite.database.db import SessionLocal
from mysite.api.auth import get_current_user
from sqlalchemy.orm import Session
from typing import List



user_router = APIRouter(prefix='/users', tags=['Users'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.get('/', response_model=List[UserOutputSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(User).all()


@user_router.get('/{user_id}/', response_model=UserOutputSchema)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай аккаунт жок', status_code=400)
    return user_db

@user_router.put('/me/', response_model=dict)
async def user_update(user: UserUpdateSchema,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == current_user.id).first()

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)

    db.commit()
    db.refresh(user_db)
    return {"message": "Маалыматтар озгорулду"}

@user_router.delete('/me/', response_model=dict)
async def user_delete(current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == current_user.id).first()
    if not user_db:
        raise HTTPException(detail='Мындай аккаунт жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {"message": "Аккаунт очурулду"}