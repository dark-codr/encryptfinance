from __future__ import absolute_import

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "encryptfinance.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import encryptfinance.users.signals  # noqa F401
        except ImportError:
            pass
