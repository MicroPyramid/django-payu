from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PayuConfig(AppConfig):
    name = 'payu'
    verbose_name = _("django payu")
