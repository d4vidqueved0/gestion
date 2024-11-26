from django import forms
from .models import Trabajador, ContactoEmergencia, CargaFamiliar, Cargo, Persona
from .validar_rut import validarRut
from django.contrib.auth.forms import PasswordChangeForm
from .contraseña_segura import validar_contraseña


class FormularioDatosPersonales(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'sexo', 'direccion', 'telefono']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono' : forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.skip_rut_validation = kwargs.pop('skip_rut_validation', False)
        super().__init__(*args, **kwargs)

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        len_tel = len(telefono)
    
        try:
            telefono = int(telefono)
        except:
            telefono
        if type(telefono) != int:
            raise forms.ValidationError('Ingrese solo numeros')
        if len_tel > 9 or len_tel < 9:
            raise forms.ValidationError('Ingrese el telefono sin prefijo, ejemplo: 911111111')
        if str(telefono)[:1] != '9':
            raise forms.ValidationError('Recuerde colocar el 9, ejemplo 911111111')

        return str(telefono)
    

    def clean_rut(self):

        if self.skip_rut_validation:
            return self.cleaned_data.get('rut')

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
        fields = ['cargo_fk', 'fecha_ingreso', 'departamento_fk'] 
        widgets = {
            'cargo_fk': forms.Select(attrs={'class': 'form-control'}, choices=Cargo.Cargos),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'departamento_fk': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cargo_fk': 'Cargo',
            'fecha_ingreso': 'Fecha de Ingreso',
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

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        len_tel = len(telefono)
    
        try:
            telefono = int(telefono)
        except:
            telefono
        if type(telefono) != int:
            raise forms.ValidationError('Ingrese solo numeros')
        if len_tel > 9 or len_tel < 9:
            raise forms.ValidationError('Ingrese el telefono sin prefijo, ejemplo: 911111111')
        if str(telefono)[:1] != '9':
            raise forms.ValidationError('Recuerde colocar el 9, ejemplo 911111111')

        return str(telefono)


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
        
        return rut
    


class FormularioContraseña(PasswordChangeForm):

    old_password = forms.CharField(
        label='Contraseña antigua',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        validar_contraseña(password1)
        return password2