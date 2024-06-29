from http import HTTPStatus
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from App.database import get_session
from App.schemas import Message, UserSchema, UserPublic, UserList, Token
from App.models import User
from App.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password
    )


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@auth_router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password'
        )
    
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email ou password'
        )
    
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@auth_router.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
        
    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@auth_router.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@auth_router.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    
    return db_user


@auth_router.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, 
    user: UserSchema, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions'
        )
    
    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@auth_router.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions'
        )
    
    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted!'}