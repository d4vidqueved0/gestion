from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from registro.models import Trabajador, Persona, CargaFamiliar, ContactoEmergencia
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.decorators import login_required
from registro.forms import FormularioDatosPersonales, FormularioCargaFamiliar, FormularioContactoEmergencia

# Create your views here.
@login_required
def panel(request):
    if request.user.is_authenticated :
        try:
            trabajador = request.user.trabajador
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


def eliminar(request, delete):
    print(delete)
    if delete:
        trabajador = get_object_or_404(Trabajador, pk=delete)
        trabajador.delete()
        messages.success(request, 'Trabajador eliminado correctamente')
    
    return redirect('panel:tabla')


def inicio(request):
    return render(request, 'panel/inicio.html')


def datos(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    cargasF = CargaFamiliar.objects.filter(trabajador = request.user.trabajador)
    contactoE = ContactoEmergencia.objects.filter(trabajador = request.user.trabajador)
    if request.method == 'POST':
        form = FormularioDatosPersonales(request.POST,  instance=persona, skip_rut_validation=True)
        print(form.is_valid())
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
        return render(request, 'panel/datos.html', {'form': form, 'cargasF': cargasF, 'contactoE': contactoE})
