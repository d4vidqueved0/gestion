import re
from django.core.exceptions import ValidationError

def validar_contraseña(password):
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula")
    if not re.search(r'[a-z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra minúscula")
    if not re.search(r'[0-9]', password):
        raise ValidationError("La contraseña debe contener al menos un número")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("La contraseña debe contener al menos un carácter especial")
