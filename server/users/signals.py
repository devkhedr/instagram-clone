from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q
from .models import User


@receiver(post_save, sender=User)
def delete_unverified_user(sender, instance, **kwargs):
    if not instance.is_verified:
        time_difference = timezone.now() - instance.created
        if time_difference.total_seconds() > 86400:
            users_to_delete = User.objects.filter(
                Q(is_verified=False) & Q(created__lte=timezone.now() - timezone.timedelta(days=1))
            )
            users_to_delete.delete()
