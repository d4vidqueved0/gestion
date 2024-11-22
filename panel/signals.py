from django.db.models.signals import post_delete
from django.dispatch import receiver
from registro.models import Trabajador

@receiver(post_delete, sender=Trabajador)
def eliminar_relaciones_trabajador(sender, instance, **kwargs):
 
    if instance.contacto_emergencia_fk and instance.contacto_emergencia_fk.trabajador_set.count() == 0:
        instance.contacto_emergencia_fk.delete()
    
    # Verificar si la CargaFamiliar no tiene otros Trabajadores que lo referencien
    if instance.carga_familiar_fk and instance.carga_familiar_fk.trabajador_set.count() == 0:
        instance.carga_familiar_fk.delete()

    if instance.user_fk:
        instance.user_fk.delete()

    # Opcional: Puedes hacer lo mismo para el objeto Persona si no es utilizado por otros Trabajadores
    if instance.persona_fk:
        instance.persona_fk.delete()

