from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel:panel')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if request.user.is_authenticated:
            messages.error(request, 'Antes de iniciar sesión con otro usuario cierre la sesión actual.')
            return render(request, 'usuarios/login.html')  
        if usuario is not None:
            login(request, usuario)
            return redirect('panel:panel') 
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('usuarios:login')