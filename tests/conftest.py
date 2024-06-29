import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from App.database import Base, get_session
from App.main import app
from App.models import User
from App.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'postgresql+psycopg2://helton:admin@localhost:5432/fastapi'
    )
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)


@pytest.fixture()
def user(session):
    user = User(username='Tinna', email='tinna@gmail.com', password='Tinna123')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def usertest(session):
    user = User(
        username='Tina',
        email='tina@gmail.com',
        password=get_password_hash('Tinna123'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture()
def token(client, usertest):
    response = client.post(
        '/auth/token',
        data={'username': usertest.email, 'password': usertest.clean_password},
    )
    return response.json()['access_token']
