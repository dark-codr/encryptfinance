from django.contrib import admin
from .models import Wallet
from .forms import WalletForm
# Register your models here.

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    form = WalletForm
    list_display = ["owner", "walletID", "qrcode", "active"]
    list_filter = ["active"]
    list_display_links = ["owner", "walletID"]
    list_editable = ["active", "qrcode"]
    class Meta:
        model = Wallet
