from __future__ import absolute_import

from decimal import Decimal

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from encryptfinance.users.models import UserProfile, UserVerify

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User



class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'username']

        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
            "email": {"unique": _("This email has already been used.")}
        }


    def save(self, commit=True):
        user = super().save(commit=False)
        user.balance = Decimal(0.00)
        email = user.email
        if commit:
            user.save()
            # send_mail(
            #     'New User',
            #     f"{user.username} just registered with this email now",
            #     'noreply@encryptfinance.net',
            #     ['admin@encryptfinance.net'],
            #     fail_silently=False,
            # )
        return user


class UserPersonalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", 'middle_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['passport', 'bank', 'account_no', 'routing_no', 'nationality', 'phone']




class UserVerifyForm(forms.ModelForm):
    class Meta:
        model = UserVerify
        fields = ['id_type', 'id_front', 'id_back', 'ssn']



