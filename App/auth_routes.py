from http import HTTPStatus
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from App.database import get_session
from App.schemas import Message, UserSchema, UserPublic, UserList
from App.models import User


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá Mundo!'}


@auth_router.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session = Depends(get_session)):
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

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
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
async def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
        )
    
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)

    return db_user


@auth_router.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
        )
    
    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted!'}