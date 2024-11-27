
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


def client():
    client = Client()
    

def test_end_to_end(client):
    response = client.post('/', {'username': '18071987-3', 'password': 'cOntraseÑa#335'})
    assert response.url == '/panel/'

    url = reverse('panel:tabla')
    response = client.get(url)
    assert 'Tabla trabajadores' in response.content.decode()

    user = User.objects.get(username="18071987-3")
    persona = user.trabajador.persona_fk
    url = reverse('panel:datos', args=[persona.pk])
    response = client.get(url)
    assert 'Mis datos'  in response.content.decode()
    assert '18071987-3'  in response.content.decode()

    url = reverse('panel:agregar_carga_familiar')
    response = client.post(url, {'rut':'23789961-1', 'nombre': 'Augusto', 'sexo': 'Masculino', 'parentesco': 'Tío'})
    assert 'El R.U.T. no es válido.' in response.content.decode()
    

    response = client.post(url, {'rut':'23789961-K', 'nombre': 'Augusto', 'sexo': 'Masculino', 'parentesco': 'Tío'})
    assert response.status_code == 302
    response = client.get(reverse('panel:datos', args=[persona.pk]))
    assert  ' Se agrego correctamente la carga familiar' in response.content.decode()


    url = reverse('panel:agregar_contacto_emergencia')
    response = client.post(url, {'nombre': 'Sebastian', 'relacion': 'Padre', 'telefono': '11111111'})
    assert 'Ingrese el telefono sin prefijo, ejemplo: 911111111' in response.content.decode()

    response = client.post(url, {'nombre': 'Sebastian', 'relacion': 'Padre', 'telefono': '911111111'})
    assert response.status_code == 302
    response = client.get(reverse('panel:datos', args=[persona.pk]))
    assert 'Se agrego correctamente el contacto de emergencia' in response.content.decode()

    
