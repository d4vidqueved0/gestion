from django import forms
from .models import Trabajador, Departamento, ContactoEmergencia, CargaFamiliar, Cargo, Persona
from .validar_rut import validarRut

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

    def clean_rut(self):

        rut = self.cleaned_data.get('rut')
        
        rut = rut.replace(".", "").replace(",", "")

        rut_aux = ""
        for num in rut:
            if num == '-':
                break
            else:
                rut_aux += num

        
        if not rut_aux.isnumeric()  :  
            raise forms.ValidationError("El R.U.T. debe contener solo números y un dígito verificador.")
        
        if  not '-' in rut:
            raise forms.ValidationError("Debe ingresar el R.U.T. con el formato 11111111-1")

        if not validarRut(rut):
            raise forms.ValidationError("El R.U.T. no es válido.")

        if Persona.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El R.U.T. ya se encuentra ingresado.")

        return rut

        


class FormularioDatosLaborales(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['cargo_fk', 'fecha_ingreso_fk', 'departamento_fk'] 
        widgets = {
            'cargo_fk': forms.Select(attrs={'class': 'form-control'}, choices=Cargo.Cargos),
            'fecha_ingreso_fk': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'departamento_fk': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cargo_fk': 'Cargo',
            'fecha_ingreso_fk': 'Fecha de Ingreso',
            'departamento_fk': 'Departamento',
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

    def clean_rut(self):

        rut = self.cleaned_data.get('rut')
        
        rut = rut.replace(".", "").replace(",", "")

        rut_aux = ""
        for num in rut:
            if num == '-':
                break
            else:
                rut_aux += num

        
        if not rut_aux.isnumeric()  :  
            raise forms.ValidationError("El R.U.T. debe contener solo números y un dígito verificador.")
        
        if  not '-' in rut:
            raise forms.ValidationError("Debe ingresar el R.U.T. con el formato 11111111-1")

        if not validarRut(rut):
            raise forms.ValidationError("El R.U.T. no es válido.")

        if CargaFamiliar.objects.filter(rut=rut).exists():
            raise forms.ValidationError("El R.U.T. ya se encuentra ingresado.")

        return rut