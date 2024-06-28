from http import HTTPStatus

from App.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/auth/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/auth/users/',
        json={
            'username': 'elton',
            'email': 'elton@gmail.com',
            'password': '123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'elton',
        'email': 'elton@gmail.com',
    }


def test_read_users(client):
    response = client.get('/auth/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_not_found(client):
    response = client.get('/auth/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/auth/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/auth/users/1',
        json={
            'username': 'Hulitos',
            'email': 'hulitos@gmail.com',
            'password': 'Hulitos123',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Hulitos',
        'email': 'hulitos@gmail.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/auth/users/10',
        json={
            'username': 'Hulitos',
            'email': 'hulitos@gmail.com',
            'password': 'Hulitos123',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/auth/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_not_found(client):
    response = client.delete('/auth/users/11')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
