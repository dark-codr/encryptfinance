from django.db.models import F
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import UserProfile, UserVerify


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_verify(sender, instance, created, *args, **kwargs):
    if created:
      UserVerify.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_verify(sender, instance, created, *args, **kwargs):
    instance.userverify.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
      UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, *args, **kwargs):
    instance.userprofile.save()