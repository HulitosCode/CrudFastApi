import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from App.app import app
from App.database import Base, get_session
from App.models import User
from App.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session(engine):
    # Cria todas as tabelas definidas no metadata
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session
        # Desfaz todas as transações pendentes
        session.rollback()

    # Remove todas as tabelas após o teste
    Base.metadata.drop_all(bind=engine)
    # Opcional: Recria as tabelas, se necessário
    Base.metadata.create_all(bind=engine)


# Resolvendo problema de lentidao na execussao dos testes
@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg2') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        yield _engine


@pytest.fixture()
def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture()
def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
