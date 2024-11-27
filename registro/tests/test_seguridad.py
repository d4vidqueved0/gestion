import pytest
from django.test import Client
from django.contrib.auth. models import User
from axes.models import AccessAttempt

@pytest.fixture
def user():
    AccessAttempt.objects.filter(username='test').delete()
    User.objects.filter(username='test').delete()
    return User.objects.create_user(username = 'test', password='test')

def client():
    client = Client()
    return client

def test_fuerza_bruta(client):
    for i in range(3):
        response = client.post('/', {'username': 'test', 'password': 'TEST'})
    assert  'Tu cuenta ha sido bloqueada' in response.content.decode()


def test_view_restringida(client):
    url = '/panel/'
    response = client.get(url)
    assert response.status_code == 302

    AccessAttempt.objects.filter(username='test').delete()
    response = client.post('/', {'username': 'test', 'password': 'test'})
    assert response.url == '/panel/'


def test_contraseña_encriptada(user):
    assert user.password != 'test'
    assert user.check_password('test')
