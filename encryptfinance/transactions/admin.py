from __future__ import absolute_import

from django.contrib import admin

from .models import Deposit, Withdrawal, Support
from .forms import DepositForm, WithdrawalForm

# Register your models here.
@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    # form = DepositForm
    list_display = ["__str__", "amount", "approval", "deposited", "created"]
    list_filter = ["approval", "created"]
    list_editable = ["approval", "amount", "deposited"]
    class Meta:
        model = Deposit

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    form = WithdrawalForm
    list_display = ["__str__", "amount", "wallet_id", "approval", "withdrawn", "created"]
    list_filter = ["approval", "created"]
    list_editable = ["approval", "withdrawn"]
    class Meta:
        model = Withdrawal



admin.site.register(Support)
