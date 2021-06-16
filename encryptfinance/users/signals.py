from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
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
    # print("profile_id", profile_id)
    if profile_id is not None:
        recommended_by_profile = UserProfile.objects.get(id=profile_id)
        recommender_email = recommended_by_profile.user.email
        registered_user = User.objects.get(id=user.id)
        registered_profile = UserProfile.objects.get(user=registered_user)
        registered_profile.recommended_by = recommended_by_profile.user
        registered_profile.save()
        email = (
            (
                f"New User Registered with {profile_id}",
                f"{registered_user.username} just registered with this referrer  \n User: {recommended_by_profile.user.username}.",
                "noreply@encryptfinance.net",
                ["admin@encryptfinance.net"],
            ),

            (
                f"New Referrer Registered",
                f"{registered_user.username} just registered with your referrer link. \n User: {recommended_by_profile.user.username}.",
                "noreply@encryptfinance.net",
                [recommended_by_profile.user.email],
            ),

            (
                f'Welcome {registered_user.username}',
                f"{registered_user.username} We are happy to have you with us. \n\nPlease Note: You were referred by {recommended_by_profile}.",
                "noreply@encryptfinance.net",
                [registered_user.email],
            )
        )
        return send_mass_mail(email, fail_silently=False)
    else:
        return send_mail(
            f"New User Registered without Referral",
            f"{user.username} just registered now with email: {user.email}",
            "noreply@encryptfinance.net",
            ["admin@encryptfinance.net"],
            fail_silently=False
        )
    