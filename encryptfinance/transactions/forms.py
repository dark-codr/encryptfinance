from __future__ import absolute_import

from django.core.mail import send_mail
from django import forms
from .models import Deposit, Withdrawal, User, RecoverFunds, Support

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["plan", "amount"]

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['amount'].widget.attrs['placeholder'] = 'Min $50.00 - $100,000.00 Max'


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount", "wallet_id"]

    def save(self, commit=True):
        form = super(WithdrawalForm, self).save(commit=False)
        if commit and form.amount < form.withdrawer.balance:
            form.save()
        return form
            


class RecoverForm(forms.ModelForm):
    class Meta:
        model = RecoverFunds
        fields = ["amount", "issue_date", "previous_broker", "wallet_id"]

            

class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ["issue"]