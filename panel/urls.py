from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('panel/', views.panel, name='panel'),
    path('tabla/?page=1', views.tabla, name='tabla'),
    path('eliminar/<int:delete>/', views.eliminar, name='eliminar'),
    path('', views.inicio, name='inicio')
]