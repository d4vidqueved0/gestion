import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

@pytest.fixture
def user():
    User.objects.filter(username="testuser").delete()
    return User.objects.create_user(username="testuser", password="12345")

@pytest.fixture
def client(user):
    client = Client()
    client.login(username="testuser", password="12345")
    return client

def test_panel_view(client):
    url = reverse('panel:panel') 
    response = client.get(url)
    assert response.status_code == 200
    assert 'Resumen trabajadores' in response.content.decode()


