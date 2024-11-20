from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def panel(request):
    if request.user.is_authenticated :
        try:
            trabajador = request.user.trabajador
        except:
            return render(request, 'panel/panel.html')

        
        
        return render(request, 'panel/panel.html', {'trabajador': trabajador})

    else:
        return redirect('usuarios:login')