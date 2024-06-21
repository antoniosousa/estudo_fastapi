from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Olá mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'email': 'teste@teste.com.br',
            'password': 'teste@123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'teste',
        'email': 'teste@teste.com.br',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'users': [
            {
                'username': 'teste',
                'email': 'teste@teste.com.br',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1/',
        json={
            'username': 'atualizado',
            'email': 'teste@teste.com.br',
            'password': 'teste@123',
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'atualizado',
        'email': 'teste@teste.com.br',
    }


def test_user_update_while_id_does_not_exist_and_negative(client):
    response2 = client.put(
        '/users/2/',
        json={
            'username': 'atualizado',
            'email': 'teste@teste.com.br',
            'password': 'teste@123',
        },
    )
    response_1 = client.put(
        '/users/-1/',
        json={
            'username': 'atualizado',
            'email': 'teste@teste.com.br',
            'password': 'teste@123',
        },
    )

    assert (
        response2.status_code == HTTPStatus.NOT_FOUND == response_1.status_code
    )
    assert (
        response2.json() == {'detail': 'User not found'} == response_1.json()
    )


def test_read_user_by_id(client):
    response = client.get('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'atualizado',
        'email': 'teste@teste.com.br',
    }


def test_read_user_by_id_while_id_does_not_exist_and_negative(client):
    response1 = client.get('/users/2/')
    response2 = client.get('/users/-1/')

    assert (
        response1.status_code == HTTPStatus.NOT_FOUND == response2.status_code
    )
    assert (
        response2.json() == {'detail': 'User not found'} == response1.json()
    )


def test_delete_user(client):
    response = client.delete('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'User deleted'}


def test_user_delete_while_id_does_not_exist_and_negative(client):
    response2 = client.delete('/users/2/')
    response1 = client.delete('/users/-1/')

    assert (
        response2.status_code == HTTPStatus.NOT_FOUND == response1.status_code
    )
    assert (
        response2.json() == {'detail': 'User not found'} == response1.json()
    )
