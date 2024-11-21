from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.panel, name='panel'),
    path('tabla/?page=1', views.tabla, name='tabla')
]