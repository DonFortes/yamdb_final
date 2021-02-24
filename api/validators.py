from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def year_validator(value):
    if value < 1700 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
