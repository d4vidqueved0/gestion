from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from axes.models import AccessAttempt
from django.contrib.auth.models import User



def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel:panel')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
                messages.info(request, 'No existe un trabajador con ese RUT')
                return render(request, 'usuarios/login.html')
        
        intentos_fallidos = AccessAttempt.objects.filter(username=username).count()
        maximo_intentos = 2
        intentos_disponibles = maximo_intentos - intentos_fallidos
            
        usuario = authenticate(request, username=username, password=password) 

        if usuario is not None:
            login(request, usuario)
            return redirect('panel:panel') 
        elif intentos_disponibles > 0:
                messages.error(request, f'RUT o contraseña incorrectos. Te quedan {intentos_disponibles} intentos antes de que se bloquee la cuenta')
    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')

def bloqueo(request):
    return render(request, 'usuarios/bloqueo.html')