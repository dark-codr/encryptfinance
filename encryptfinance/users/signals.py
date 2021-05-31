from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.db.models import F
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


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    profile_id = request.session.get("ref_profile")
    print("profile_id", profile_id)
    if profile_id is not None:
        recommended_by_profile = UserProfile.objects.get(id=profile_id)
        recommender_email = recommended_by_profile.user.email
        registered_user = User.objects.get(id=user.id)
        registered_profile = UserProfile.objects.get(user=registered_user)
        registered_profile.recommended_by = recommended_by_profile.user
        registered_profile.save()
        send_mail(
            f"New User Registered with {profile_id} code",
            f"{user.username} just registered with this referrer  \n User: {recommended_by_profile}  now",
            "noreply@encryptfinance.net",
            ["admin@encryptfinance.net", recommender_email, registered_user.email],
            fail_silently=False,
        )
