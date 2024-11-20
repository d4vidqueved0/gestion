from django import forms
from .models import Trabajador, Departamento, ContactoEmergencia, CargaFamiliar, Cargo, Persona

class FormularioDatosPersonales(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'rut', 'sexo', 'direccion', 'telefono']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class FormularioDatosLaborales(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['cargo_fk', 'fecha_ingreso_fk', 'departamento_fk'] 
        widgets = {
            'cargo_fk': forms.Select(attrs={'class': 'form-control'}, choices=Cargo.Cargos),
            'fecha_ingreso_fk': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'departamento_fk': forms.Select(attrs={'class': 'form-control'}),
        }




class FormularioContactoEmergencia(forms.ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = ['nombre', 'relacion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'relacion': forms.Select(attrs={'class': 'form-control'}, choices=ContactoEmergencia.Relaciones),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormularioCargaFamiliar(forms.ModelForm):
    class Meta:
        model = CargaFamiliar
        fields = ['rut', 'nombre', 'sexo', 'parentesco']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'parentesco': forms.Select(attrs={'class': 'form-control'}, choices=CargaFamiliar.Parentescos),
        }
