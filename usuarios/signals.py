from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from axes.models import AccessAttempt

@receiver(user_logged_in)
def reset_failed_attempts(sender, request, user, **kwargs):
    AccessAttempt.objects.filter(username=user.username).delete()
