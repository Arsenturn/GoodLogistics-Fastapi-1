from fastapi import APIRouter, HTTPException, Depends, Body
from mysite.database.models import User, RefreshToken
from mysite.database.schema import (
    UserRegisterSchema, UserLoginSchema, CurrentUserSchema, UserOutputSchema
)
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from mysite.config import (
    SECRET_KEY, ALGORITHM,
    ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
)
from datetime import timedelta, datetime
from typing import Optional
from jose import jwt, JWTError


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


credentials_exception = HTTPException(
    status_code=401,
    detail='Access token туура эмес же мөөнөтү бүттү',
    headers={'WWW-Authenticate': 'Bearer'},
)


async def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        subject = payload.get('sub')

        if subject is None:
            raise credentials_exception

        user_id = int(subject)
    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise credentials_exception

    return user_db


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expires = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


def get_token_data(user: User):
    return {'sub': str(user.id), 'username': user.username, 'status': user.status.value}


@auth_router.post('/register/', response_model=dict)
async def register(user: UserRegisterSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    email_db = db.query(User).filter(User.email == user.email).first()
    if user_db or email_db:
        raise HTTPException(detail='Мындай username же email бар экен', status_code=400)

    hash_password = get_password_hash(user.password)
    user_data = User(
        username=user.username,
        email=user.email,
        password=hash_password
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'Сиз ийгиликтүү регистрация болдуңуз'}


@auth_router.post('/login/', response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(detail='Сиз жазган маалымат туура эмес', status_code=401)

    token_data = get_token_data(user_db)

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'user': CurrentUserSchema(id=user_db.id, username=user_db.username, status=user_db.status)
    }


@auth_router.post('/refresh/', response_model=dict)
async def refresh(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    user_db = stored_token.token_user
    token_data = get_token_data(user_db)

    access_token = create_access_token(token_data)

    return {'access_token': access_token, 'token_type': 'Bearer'}


@auth_router.post('/logout/', response_model=dict)
async def logout(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    db.delete(stored_token)
    db.commit()

    return {'message': 'Ийгиликтүү чыгып кеттиңиз'}


@auth_router.get('/verify/', response_model=CurrentUserSchema)
async def verify_access_token(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.get('/me/', response_model=UserOutputSchema)
async def user_me(profile: User = Depends(get_current_user)):
    return profile