from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):
    Areas = (
        ('',''),
        ('Area1','Area1'),
        ('Area2','Area2'),
    )
    nombre_area = models.CharField(max_length=30, choices=Areas)

    def __str__(self):
        return self.nombre_area


class Departamento(models.Model):
    Departamentos = (
        ('',''),
        ('Departamento1','Departamento1'),
        ('Departamento2','Departamento2'),
        ('Departamento3','Departamento3'),
        ('Departamento4','Departamento4'),
    )
    nombre_departamento = models.CharField(max_length=30, choices=Departamentos)
    area_fk = models.ForeignKey(Area, models.CASCADE)

    def __str__(self):
        return self.nombre_departamento


class Cargo(models.Model):
    Cargos = (
        ('', ''),
        ('Jefe RR.HH', 'Jefe RR.HH'),
        ('Personal RR.HH', 'Personal RR.HH'),
        ('Trabajador', 'Trabajador'),
    )
    nombre_cargo = models.CharField(max_length=30, choices=Cargos)

    def __str__(self):
        return self.nombre_cargo


class ContactoEmergencia(models.Model):
    Relaciones = (
        ('', ''),
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Hijo', 'Hijo'),
        ('Hija', 'Hija'),
        ('Esposo', 'Esposo'),
        ('Esposa', 'Esposa'),
        ('Hermano', 'Hermano'),
        ('Hermana', 'Hermana'),
        ('Abuelo', 'Abuelo'),
        ('Abuela', 'Abuela'),
        ('Nieto', 'Nieto'),
        ('Nieta', 'Nieta'),
        ('Tío', 'Tío'),
        ('Tía', 'Tía'),
        ('Sobrino', 'Sobrino'),
        ('Sobrina', 'Sobrina'),
        ('Primo', 'Primo'),
        ('Prima', 'Prima'),
        ('Otro', 'Otro'),
        
    )

    nombre = models.CharField(max_length=100)
    relacion = models.CharField(max_length=20, choices=Relaciones)
    telefono = models.CharField(max_length=15)


class CargaFamiliar(models.Model):
    Parentescos = (
        ('', ''),
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Hijo', 'Hijo'),
        ('Hija', 'Hija'),
        ('Esposo', 'Esposo'),
        ('Esposa', 'Esposa'),
        ('Hermano', 'Hermano'),
        ('Hermana', 'Hermana'),
        ('Abuelo', 'Abuelo'),
        ('Abuela', 'Abuela'),
        ('Nieto', 'Nieto'),
        ('Nieta', 'Nieta'),
        ('Tío', 'Tío'),
        ('Tía', 'Tía'),
        ('Sobrino', 'Sobrino'),
        ('Sobrina', 'Sobrina'),
        ('Primo', 'Primo'),
        ('Prima', 'Prima'),
        ('Otro', 'Otro'),
    )
    Sexo = (
        ('', ''),
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    )
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=Sexo)
    parentesco = models.CharField(max_length=20, choices=Parentescos)



class Persona(models.Model):
    Sexo = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    )
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    sexo = models.CharField(max_length=10, choices=Sexo)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)




class Trabajador(models.Model):
    persona_fk = models.OneToOneField(Persona,on_delete=models.CASCADE)
    fecha_ingreso_fk = models.DateField(null=True)
    cargo_fk = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    contacto_emergencia_fk = models.ForeignKey(ContactoEmergencia, on_delete=models.CASCADE)
    carga_familiar_fk = models.ForeignKey(CargaFamiliar, on_delete=models.CASCADE)
    departamento_fk = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    user_fk = models.OneToOneField(User, on_delete=models.CASCADE)