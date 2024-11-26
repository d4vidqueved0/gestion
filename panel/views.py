from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from registro.models import Trabajador, Persona, CargaFamiliar, ContactoEmergencia
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.decorators import login_required
from registro.forms import FormularioDatosPersonales, FormularioCargaFamiliar, FormularioContactoEmergencia, FormularioContraseña, FormularioDatosLaborales
from django.contrib.auth import update_session_auth_hash


# Create your views here.
@login_required
def panel(request):
    if request.user.is_authenticated :
        try:
            trabajador = request.user.trabajador
            print(trabajador.contraseña_cambiada)
            if not trabajador.contraseña_cambiada:
                messages.warning(request, 'Antes de continuar debe cambiar la contraseña predeterminada. La contraseña es su apellido paterno combinado con el materno ejemplo: SotoPerez')
                return redirect('panel:cambiar_contraseña')
        except:
            return render(request, 'panel/panel.html')        
        return render(request, 'panel/panel.html', {'trabajador': trabajador})
    else:
        return redirect('usuarios:login')
    
@login_required
def tabla(request):
    
    order = request.GET.get('order', 'persona_fk__rut')
    query = request.GET.get('search', '')

    trabajadores = Trabajador.objects.all()

    if query:
        trabajadores = trabajadores.filter(
            Q(persona_fk__nombres__icontains=query) |
            Q(persona_fk__apellido_paterno__icontains=query) |
            Q(persona_fk__apellido_materno__icontains=query) |
            Q(cargo_fk__nombre_cargo__icontains=query) |
            Q(persona_fk__sexo__icontains=query)
        )

    trabajadores = trabajadores.order_by(order)

    paginator = Paginator(trabajadores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'panel/tabla_trabajadores.html', {'page_obj': page_obj, 'query': query})

@login_required
def eliminar(request, delete):
    if delete:
        trabajador = get_object_or_404(Trabajador, pk=delete)
        trabajador.delete()
        messages.success(request, 'Trabajador eliminado correctamente')
    
    return redirect('panel:tabla')


@login_required
def datos(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if request.user.trabajador.persona_fk.pk == persona.pk:
        cargasF = CargaFamiliar.objects.filter(trabajador_fk = request.user.trabajador)
        contactoE = ContactoEmergencia.objects.filter(trabajador_fk = request.user.trabajador)
        if request.method == 'POST':
            form = FormularioDatosPersonales(request.POST,  instance=persona, skip_rut_validation=True)
            if form.is_valid():
                form.save()
                form = FormularioDatosPersonales(instance=persona)
                messages.success(request, 'Datos personales actualizados correctamente.')
                return redirect('panel:panel')
            else:
                form = FormularioDatosPersonales(instance=persona)
                return render(request, 'panel/datos.html', {'form': form, 'cargasF': cargasF, 'contactoE': contactoE})

        else:
            form = FormularioDatosPersonales(instance=persona)
            return render(request, 'panel/datos.html', {'form': form, 'cargasF': cargasF, 'contactoE': contactoE })
    else:
        messages.error(request, 'No puede acceder a informacion que no está asociada a su cuenta')
        return redirect('usuarios:login')


@login_required
def editar_carga(request, pk):
    carga = get_object_or_404(CargaFamiliar, pk=pk)
    if request.user.trabajador == carga.trabajador_fk:
        if request.method == 'POST':
            formC = FormularioCargaFamiliar(request.POST, instance=carga)
            if formC.is_valid():
                formC.save()
                return redirect('panel:datos', pk=request.user.trabajador.persona_fk.pk)
        else:
            formC = FormularioCargaFamiliar(instance=carga)
            return render(request, 'panel/editar_carga.html', {'formC': formC})
    else:
        messages.error(request, 'No puede editar una carga familiar que no está asociada a su cuenta')
        return redirect('panel:panel')
    
@login_required
def editar_contacto(request, pk):
    contacto = get_object_or_404(ContactoEmergencia, pk=pk)
    if request.user.trabajador == contacto.trabajador_fk:
        if request.method == 'POST':
            formE = FormularioContactoEmergencia(request.POST, instance=contacto)
            if formE.is_valid():
                formE.save()
                return redirect('panel:datos', pk=request.user.trabajador.persona_fk.pk)
        else:
            formE = FormularioContactoEmergencia(instance=contacto)
            return render(request, 'panel/editar_contacto.html', {'formE': formE})
    else:
        messages.error(request, 'No puede editar un contacto que no está asociado a su cuenta')
        return redirect('panel:panel')
    
@login_required
def agregar_carga_familiar(request):
    cargas = CargaFamiliar.objects.filter(trabajador_fk = request.user.trabajador)
    if cargas.count() >= 5:
        messages.warning(request, 'No se pueden agregar más de 5 cargas familiares.')
        return redirect('panel:datos', pk=request.user.trabajador.persona_fk.pk)
    else:
        if request.method == 'GET':
            form = FormularioCargaFamiliar()
            return render(request, 'registro/formulario_carga_familiar.html', {'form': form})
        else:
            form = FormularioCargaFamiliar(request.POST)
            cargas = CargaFamiliar.objects.filter(trabajador_fk = request.user.trabajador)
            if form.is_valid():
                if cargas.filter(rut=form.cleaned_data['rut']).exists():
                    messages.warning(request, 'Ya existe una carga familiar con ese RUT.')
                    return render(request, 'registro/formulario_carga_familiar.html', {'form': form})
                else:
                    trabajador = request.user.trabajador
                    print(form.cleaned_data)
                    carga = CargaFamiliar.objects.create(
                        **form.cleaned_data,
                        trabajador_fk= trabajador
                    )
                    return render(request, 'panel/datos.html', {'pk': request.user.trabajador.persona_fk.pk})
            else:
                return render(request, 'registro/formulario_carga_familiar.html', {'form': form})
        
@login_required
def agregar_contacto_emergencia(request):
    contactos = ContactoEmergencia.objects.filter(trabajador_fk = request.user.trabajador)
    if contactos.count() >= 3:
        messages.warning(request, 'No se pueden agregar más de 3 contactos de emergencia.')
        return redirect('panel:datos', pk=request.user.trabajador.persona_fk.pk)
    else:
        if request.method == 'GET':
            form = FormularioContactoEmergencia()
            return render(request, 'registro/formulario_contacto_emergencia.html', {'form': form})
        else:
            form = FormularioContactoEmergencia(request.POST)
            if form.is_valid():
                trabajador = request.user.trabajador
                print(form.cleaned_data)
                contacto = ContactoEmergencia.objects.create(
                    **form.cleaned_data,
                    trabajador_fk= trabajador
                )
                messages.success(request, 'Se agrego correctamente el contacto de emergencia')
                return redirect('panel:datos', pk=request.user.trabajador.persona_fk.pk)
            else:
                return render(request, 'registro/formulario_contacto_emergencia.html', {'form': form})
        

        
@login_required
def eliminar_carga(request, pk):
    carga = get_object_or_404(CargaFamiliar, pk=pk)
    carga.delete()
    messages.success(request, 'Carga familiar eliminada correctamente.')
    return redirect('panel:datos', pk=request.user.trabajador.persona_fk.pk)

@login_required
def eliminar_contacto(request, pk):
    contacto = get_object_or_404(ContactoEmergencia, pk=pk)
    contacto.delete()
    messages.success(request, 'Contacto de emergencia eliminado correctamente.')
    return redirect('panel:datos', pk=request.user.trabajador.persona_fk.pk)


def cambiar_contraseña(request):
    if request.method == 'POST':
        form = FormularioContraseña(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            user.trabajador.contraseña_cambiada = True
            user.trabajador.save()
            messages.success(request, 'La contraseña se cambió correctamente.')
            return redirect('panel:panel')
    else:
        form = FormularioContraseña(request.user)
    return render(request, 'panel/cambiar_contraseña.html', {'form': form})