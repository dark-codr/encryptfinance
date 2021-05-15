from __future__ import absolute_import

from django import forms

from .models import Wallet


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['owner', "walletID", "qrcode", "active"]