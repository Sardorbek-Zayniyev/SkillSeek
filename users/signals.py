from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile_or_update_user(sender, instance, created, **kwargs):
    # profile creation
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name,
        )
    # updating user
    else:
        instance.profile.save()


@receiver(post_delete, sender=Profile)
def deleting_user(sender, instance, **kwargs):
    instance.delete()
