from __future__ import absolute_import

from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
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

    # def clean_first_name(self):
    #     if "first_name":
    #     # add .title to make field first letter in each word uppercase
    #         return self.cleaned_data['first_name'].title()

    # def clean_middle_name(self):
    #     if "middle_name":
    #     # add .title to make field first letter in each word uppercase
    #         return self.cleaned_data['middle_name'].title()
    #     return self.cleaned_data["middle_name"]
        
    # def clean_last_name(self):
    #     if "last_name":
    #     # add .title to make field first letter in each word uppercase
    #         return self.cleaned_data['last_name'].title()


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
        fields = ['id_type', 'id_front', 'id_back', 'bank_statement', 'ssn']



