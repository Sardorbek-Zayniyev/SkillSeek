from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings

from .models import User, Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    # creating profile
    if created:
        profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name,
        )
        #sending eMail
        subject = 'Welcome to SkillSeek'
        message = 'We are glad you are here!'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [profile.email],
            fail_silently=False,
        )

    #  updating profile
    else:
        if not hasattr(instance, '_profile_updated'):
            instance._profile_updated = True
            profile = instance.profile
            profile.username = instance.username
            profile.email = instance.email
            profile.name = instance.first_name
            profile.save()


@receiver(post_delete, sender=Profile)
def deleting_user(sender, instance, **kwargs):
    try:
        if instance.user and not hasattr(instance, '_user_deleted'):
            instance._user_deleted = True
            instance.user.delete()
    except ObjectDoesNotExist:
        pass
