from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('panel/', views.panel, name='panel'),
    path('tabla/?page=1', views.tabla, name='tabla'),
    path('eliminar/<int:delete>/', views.eliminar, name='eliminar'),
    path('datos/<int:pk>/', views.datos, name='datos'),
    path('editar_carga/<int:pk>/', views.editar_carga, name='editar_carga'),
    path('editar_contacto/<int:pk>/', views.editar_contacto, name='editar_contacto'),
    path('eliminar_carga/<int:pk>/', views.eliminar_carga, name='eliminar_carga'),
    path('eliminar_contacto/<int:pk>/', views.eliminar_contacto, name='eliminar_contacto'),
    path('agregar_carga_familiar/', views.agregar_carga_familiar, name='agregar_carga_familiar'),
    path('agregar_contacto_emergencia/', views.agregar_contacto_emergencia, name='agregar_contacto_emergencia'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña')
]