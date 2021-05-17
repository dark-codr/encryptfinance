from django.db import models

# Create your models here.
import os
import random
from datetime import datetime, timedelta
from django.utils import timezone

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import (
    CharField,
    DateField,
    DecimalField,
    ForeignKey,
    IntegerField,
    OneToOneField,
    TextField,
    CASCADE,
    SET_NULL,
)
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)

from model_utils.models import TimeStampedModel
from ckeditor.fields import RichTextField

User = settings.AUTH_USER_MODEL

VERIFIED = "VERIFIED"
PENDING = "PENDING"
FAILED = "FAILED"
APPROVAL = (
    (VERIFIED, "VERIFIED"),
    (PENDING, "PENDING"),
    (FAILED, "FAILED"),
)

DAILY = "DAILY"
SILVER = "SILVER"
GOLD = "GOLD"
DIAMOND = "DIAMOND"
PLAN = (
    (DAILY, "DAILY"),
    (SILVER, "SILVER"),
    (GOLD, "GOLD",),
    (DIAMOND, "DIAMOND")
)



class Deposit(TimeStampedModel):
    depositor = ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name="deposits")
    approval = CharField(choices=APPROVAL, default=PENDING, max_length=15, null=True, blank=True)
    plan = CharField(choices=PLAN, default=DAILY, max_length=15, null=True, blank=True)
    amount = DecimalField(_('Deposited Amount'), decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('50.00')), MaxValueValidator(Decimal('1000000.00'))], help_text="min-amount: $50, max-amount: $100000", null=True, blank=True)
    deposited = DateField(default=datetime.now)

    class Meta:
        verbose_name = "Deposit"
        verbose_name_plural = "Deposits"
        ordering = ["-modified"]

    def __str__(self):
        return self.depositor.username


class Withdrawal(TimeStampedModel):
    withdrawer = ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name="withdrawals")
    approval = CharField(choices=APPROVAL, default=PENDING, max_length=15, null=True, blank=True)
    amount = DecimalField(_('Withdrawal Amount'), decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('100.00')), MaxValueValidator(Decimal('1000000.00'))], help_text="min-amount: $100, max-amount: $100000", null=True, blank=True)
    wallet_id = CharField(max_length=255, null=True, blank=True)
    withdrawn = DateField(default=datetime.now)

    class Meta:
        verbose_name = "Withdrawal"
        verbose_name_plural = "Withdrawals"
        ordering = ["-modified"]

    def __str__(self):
        return self.withdrawer


class RecoverFunds(TimeStampedModel):
    requester = ForeignKey(User, on_delete=CASCADE, null=True)
    approval = CharField(choices=APPROVAL, default=PENDING, max_length=15, null=True, blank=True)
    amount = DecimalField(_('Lost Amount'), decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('100.00')), MaxValueValidator(Decimal('1000000.00'))], help_text="min-amount: $100, max-amount: $100000", null=True, blank=True)
    wallet_id = CharField(max_length=255, null=True, blank=True)
    previous_broker = CharField(max_length=255, null=True, blank=True)
    issue_date = DateField(default=timezone.now)
    resolved_date = DateField(default=timezone.now)

    class Meta:
        verbose_name = "Fund Recovery"
        verbose_name_plural = "Fund Recoveries"
        ordering = ["-modified"]

    def __str__(self):
        return self.requester



class Support(TimeStampedModel):
    user = ForeignKey(User, on_delete=CASCADE, null=True, related_name="supported_user")
    issue = TextField(_("Type your complains here"))

    class Meta:
        verbose_name = "Support"
        verbose_name_plural = "Supports"
        ordering = ["-modified"]

    def __str__(self):
        return self.user

