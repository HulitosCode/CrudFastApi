from pydantic import BaseModel, ConfigDict, EmailStr
from App.models import TodoState

class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

# Validar entrada de dados quando criar uma tarefa
class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


# Validar saida de dados de uma tarefa quando retornar um endpoint
class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None