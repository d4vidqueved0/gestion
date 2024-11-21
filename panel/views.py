from django.shortcuts import render, redirect
from django.contrib import messages
from registro.models import Trabajador
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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
    query = request.GET.get('search', '')

    # Filtrar los trabajadores según el término de búsqueda
    if query:
        trabajadores = Trabajador.objects.filter(
            Q(persona_fk__rut__icontains=query) |
            Q(persona_fk__nombres__icontains=query) |
            Q(persona_fk__apellido_paterno__icontains=query) |
            Q(persona_fk__apellido_materno__icontains=query)
        )
    else:
        trabajadores = Trabajador.objects.all()

    trabajadores = trabajadores.order_by('persona_fk__rut')

    paginator = Paginator(trabajadores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'panel/tabla_trabajadores.html', {'page_obj': page_obj, 'query': query})