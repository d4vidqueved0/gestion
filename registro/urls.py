from django.urls import path
from . import views

app_name = 'registro'  

urlpatterns = [
    path('datos_personales/', views.vistaDatosPersonales, name='vistaDatosPersonales'),
    path('datos_laborales/', views.vistaDatosLaborales, name='vistaDatosLaborales'),
    path('contacto_emergencia/', views.vistaContactoEmergencia, name='vistaContactoEmergencia'),
    path('carga_familiar/', views.vistaCargaFamiliar, name='vistaCargaFamiliar'),
]
