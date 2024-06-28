from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Olá mundo!'}


def test_create_user(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'user_created',
            'email': 'user_created@teste.com.br',
            'password': 'teste@123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'user_created',
        'email': 'user_created@teste.com.br',
        'id': 2,
    }


def test_create_user_while_user_already_exist(client, user):
    resp_username = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste_@teste.com.br',
            'password': 'teste@123',
        },
    )

    resp_email = client.post(
        '/users/',
        json={
            'username': 'Teste_',
            'email': 'teste@teste.com.br',
            'password': 'teste@123',
        },
    )

    assert resp_username.status_code == HTTPStatus.BAD_REQUEST
    assert resp_email.status_code == HTTPStatus.BAD_REQUEST

    assert resp_username.json() == {'detail': 'Username already exists'}

    assert resp_email.json() == {'detail': 'E-mail already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': []}


def test_read_users_whith_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
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


def test_user_update_while_user_does_not_exist(client):
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


def test_read_user_by_id(client, user):
    response = client.get('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Teste',
        'email': 'teste@teste.com.br',
    }


def test_read_user_by_id_while_user_does_not_exist(client):
    response1 = client.get('/users/2/')
    response2 = client.get('/users/-1/')

    assert (
        response1.status_code == HTTPStatus.NOT_FOUND == response2.status_code
    )
    assert response2.json() == {'detail': 'User not found'} == response1.json()


def test_delete_user(client, user):
    response = client.delete('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'User deleted'}


def test_user_delete_while_user_does_not_exist(client, user):
    response2 = client.delete('/users/2/')
    response1 = client.delete('/users/-1/')

    assert (
        response2.status_code == HTTPStatus.NOT_FOUND == response1.status_code
    )
    assert response2.json() == {'detail': 'User not found'} == response1.json()
