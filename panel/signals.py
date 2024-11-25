from django.db.models.signals import post_delete
from django.dispatch import receiver
from registro.models import Trabajador, ContactoEmergencia, CargaFamiliar

@receiver(post_delete, sender=Trabajador)
def eliminar_relaciones_trabajador(sender, instance, **kwargs):
    # Eliminar todas las instancias relacionadas de ContactoEmergencia
    contactos = ContactoEmergencia.objects.filter(trabajador_fk=instance)
    for contacto in contactos:
        contacto.delete()
    
    # Eliminar todas las instancias relacionadas de CargaFamiliar
    cargas = CargaFamiliar.objects.filter(trabajador_fk=instance)
    for carga in cargas:
        carga.delete()
    
    # Eliminar el usuario asociado si existe
    if instance.user_fk:
        instance.user_fk.delete()
    
    # Eliminar el objeto Persona si no está relacionado con otros Trabajadores
    if instance.persona_fk:
        instance.persona_fk.delete()
