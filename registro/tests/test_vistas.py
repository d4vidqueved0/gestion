import pytest
from django.urls import reverse
from django.test import Client
from registro.models import Trabajador


@pytest.fixture
def client():
    client = Client()
    client.post('/', {'username': '18071987-3', 'password': 'cOntraseÑa#335'}) 
    return client


def test_panel(client):
    url = reverse('panel:panel')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Resumen trabajadores' in response.content.decode()
    assert 'Bienvenido' in response.content.decode()


def test_resumen(client):
    url = reverse('panel:tabla')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Tabla trabajadores' in response.content.decode()


def test_mis_datos(client): 
    trabajador = Trabajador.objects.get(user_fk=client.session['_auth_user_id'])
    persona = trabajador.persona_fk.pk
    url = reverse('panel:datos', args=[persona])
    response = client.get(url)
    assert response.status_code == 200
    assert 'Mis datos' in response.content.decode()


def test_cambiar_contraseña(client):
    url = reverse('panel:cambiar_contraseña')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Cambiar contraseña' in response.content.decode()


def test_cerrar_sesion(client):
    url = reverse('usuarios:logout')
    response = client.get(url)
    assert response.url == reverse('usuarios:login')


def test_form1(client):
    url = reverse('registro:vistaDatosPersonales')
    response = client.get(url)
    assert 'Formulario de datos personales' in response.content.decode()


def test_form2(client):
    url = reverse('registro:vistaCargaFamiliar')
    response = client.get(url)
    assert 'Formulario de carga familiar' in response.content.decode()


def test_form3(client):
    url = reverse('registro:vistaContactoEmergencia')
    response = client.get(url)
    assert 'Formulario de contacto de emergencia' in response.content.decode()


def test_form4(client):
    url = reverse('registro:vistaDatosLaborales')
    response = client.get(url)
    assert 'Formulario de Datos Laborales' in response.content.decode()
