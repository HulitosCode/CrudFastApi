from http import HTTPStatus

from App.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_get_token(client, usertest):
    response = client.post(
        '/auth/token',
        data={'username': usertest.email, 'password': usertest.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Tinna',
            'email': 'tinna@gmail.com',
            'password': 'Tinna123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Tinna',
        'email': 'tinna@gmail.com',
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_not_found(client):
    response = client.get('/auth/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, usertest, token):
    response = client.put(
        f'/users/{usertest.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Tinna',
            'email': 'tinna@gmail.com',
            'password': 'Tinna123',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Tinna',
        'email': 'tinna@gmail.com',
        # 'id': usertest.id,
    }


def test_update_user_not_found(client, usertest):
    response = client.put(
        f'/users/{usertest.id}',
        json={
            'username': 'Tinna',
            'email': 'tinna@gmail.com',
            'password': 'Tinna123',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_not_found(client):
    response = client.delete('/auth/users/11')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
