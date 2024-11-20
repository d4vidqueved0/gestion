from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import FormularioDatosPersonales, FormularioContactoEmergencia, FormularioCargaFamiliar, FormularioDatosLaborales
from .models import Trabajador, Cargo, Persona, CargaFamiliar, ContactoEmergencia
from django.contrib.auth.models import User


def vistaDatosPersonales(request):
    if request.method == 'GET':
        form = FormularioDatosPersonales()
        return render(request, 'registro/formulario_datos_personales.html', {'form': form})
    else:
        form = FormularioDatosPersonales(request.POST)
        if form.is_valid():
            request.session['persona'] = form.cleaned_data
        return redirect('registro:vistaCargaFamiliar')


def vistaCargaFamiliar(request):
    if request.method == 'GET':
        form = FormularioCargaFamiliar()
        return render(request, 'registro/formulario_carga_familiar.html', {'form': form})
    else:
        form = FormularioCargaFamiliar(request.POST)
        if form.is_valid():
            request.session['carga'] = form.cleaned_data
        return redirect('registro:vistaContactoEmergencia')


def vistaContactoEmergencia(request):
    if request.method == 'GET':
        form = FormularioContactoEmergencia()
        return render(request, 'registro/formulario_contacto_emergencia.html', {'form': form})
    else:
        form = FormularioContactoEmergencia(request.POST)
        if form.is_valid():
            request.session['contacto'] = form.cleaned_data
        return redirect('registro:vistaDatosLaborales')


def vistaDatosLaborales(request):
    if request.method == 'GET':
        form = FormularioDatosLaborales()
        return render(request, 'registro/formulario_datos_laborales.html', {'form': form})
    else:
        form = FormularioDatosLaborales(request.POST)
        if form.is_valid():
            persona_data = request.session.get('persona')
            carga_data = request.session.get('carga')
            contacto_data = request.session.get('contacto')

            # Crear instancias de los modelos
            persona = Persona.objects.create(**persona_data)
            carga = CargaFamiliar.objects.create(**carga_data)
            contacto = ContactoEmergencia.objects.create(**contacto_data)

            nuevo_dato = form.save(commit=False)
            nuevo_dato.persona_fk = persona
            nuevo_dato.contacto_emergencia_fk = contacto
            nuevo_dato.carga_familiar_fk = carga

            username = f'{persona.rut}'
            password = f'{persona.apellido_paterno}{persona.apellido_materno}'
            contraseña_encriptada = make_password(password)

            user = User.objects.create(
                username=username,
                password=contraseña_encriptada
            )

            nuevo_dato.user_fk = user
            nuevo_dato.save()

            return redirect('usuarios:login')
        return render(request, 'registro/formulario_datos_laborales.html', {'form': form})
