from http import HTTPStatus


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Tinna',
            'email': 'tinna@example.com',
            'password': 'Tinna123',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}
