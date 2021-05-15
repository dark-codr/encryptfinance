from __future__ import absolute_import

import os
import random

from django.utils.translation import gettext_lazy as _
from django.db.models import (
    BooleanField,
    CharField,
    ImageField,
)

from model_utils.models import TimeStampedModel

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def qrcode_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "qrcode/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

# Create your models here.
class Wallet(TimeStampedModel):
    owner = CharField(_("Wallet Owner"), max_length=255, null=True, blank=True, unique=True)
    walletID = CharField(_("Wallet ID"), max_length=36, null=True, blank=True, unique=True)
    qrcode = ImageField(_('QR Code'), upload_to=qrcode_image_path, null=True, blank=False)
    active = BooleanField(_("Wallet is Active?"), default=False)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        ordering = ["created"]

    def __str__(self):
        return self.walletID
