from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import FormularioDatosPersonales, FormularioContactoEmergencia, FormularioCargaFamiliar, FormularioDatosLaborales
from .models import Trabajador, Cargo, Persona, CargaFamiliar, ContactoEmergencia
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def vistaDatosPersonales(request):
    if request.method == 'GET':
        form = FormularioDatosPersonales()
        return render(request, 'registro/formulario_datos_personales.html', {'form': form})
    else:
        form = FormularioDatosPersonales(request.POST)
        if form.is_valid():
            request.session['persona'] = form.cleaned_data
            return redirect('registro:vistaCargaFamiliar')
        return render(request, 'registro/formulario_datos_personales.html', {'form': form})

@login_required
def vistaCargaFamiliar(request):
    if request.method == 'GET':
        form = FormularioCargaFamiliar()
        return render(request, 'registro/formulario_carga_familiar.html', {'form': form})
    else:
        form = FormularioCargaFamiliar(request.POST)
        if form.is_valid():
            request.session['carga'] = form.cleaned_data
            return redirect('registro:vistaContactoEmergencia')
        return render(request, 'registro/formulario_carga_familiar.html', {'form': form})

@login_required
def vistaContactoEmergencia(request):
    if request.method == 'GET':
        form = FormularioContactoEmergencia()
        return render(request, 'registro/formulario_contacto_emergencia.html', {'form': form})
    else:
        form = FormularioContactoEmergencia(request.POST)
        if form.is_valid():
            request.session['contacto'] = form.cleaned_data
            return redirect('registro:vistaDatosLaborales')
        return render(request, 'registro/formulario_contacto_emergencia.html', {'form': form})

@login_required
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

            persona = Persona.objects.create(**persona_data)
    
            username = f'{persona.rut}'
            password = f'{persona.apellido_paterno}{persona.apellido_materno}'
            contraseña_encriptada = make_password(password)

            user = User.objects.create(
                username=username,
                password=contraseña_encriptada
            )
  
            trabajador = Trabajador.objects.create(
                persona_fk=persona,
                cargo_fk=form.cleaned_data['cargo_fk'],
                fecha_ingreso=form.cleaned_data['fecha_ingreso'],
                departamento_fk=form.cleaned_data['departamento_fk'],
                user_fk=user
            )

            CargaFamiliar.objects.create(
                **carga_data,
                trabajador_fk=trabajador  
            )
            ContactoEmergencia.objects.create(
                **contacto_data,
                trabajador_fk=trabajador
            )
            
            messages.success(request, 'Se creó correctamente la ficha del trabajador')
            return redirect('panel:panel')
        return render(request, 'registro/formulario_datos_laborales.html', {'form': form})



