from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


@receiver(post_delete, sender=Profile)
def deleting_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()
