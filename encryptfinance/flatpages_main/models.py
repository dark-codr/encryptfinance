from __future__ import absolute_import

import os
import random

from django.utils.translation import gettext_lazy as _
from django.db.models import (
    BooleanField,
    CharField,
    TextField,
    ImageField,
)

from model_utils.models import TimeStampedModel

# Create your models here.
class FAQ(TimeStampedModel):
    question = CharField(_("FAQ Question"), max_length=500, null=True, blank=True, unique=True)
    answer = TextField(_("FAQ Answer"), null=True, blank=True, unique=True)
    active = BooleanField(_("FAQ Active?"), default=False)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["created"]

    def __str__(self):
        return self.question
