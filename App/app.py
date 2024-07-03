from http import HTTPStatus

from fastapi import FastAPI

from App.routers import auth, users, todos
from App.schemas import Message
from App.database import engine, Base
from App.models import User, Todo


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}