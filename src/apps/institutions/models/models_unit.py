from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.common.models.base import Base
from apps.common.models.address import Address
from apps.institutions.models.models_net import NetSchools

from src.apps.users.models import CustomUser


from django.core.exceptions import ValidationError

from datetime import date
import re
from django.core.validators import RegexValidator


def validate_cnpj(value):
    """Valida formato e dígitos de
    CNPJ (00.000.000/0000-00 ou 00000000000000)
    """
    if not value:
        return
    cnpj = re.sub(r'\D', '', str(value))
    if len(cnpj) != 14:
        raise ValidationError(
            _("CNPJ deve conter exatamente 14 dígitos numéricos."))


class UnitSchool(Base, Address):

    #  Network Connection (Many units per network)
    netschools = models.ForeignKey(
        NetSchools,
        related_name='units',
        verbose_name=_("net_school_unit"),
        on_delete=models.PROTECT,
        help_text=_("Find")
    )
    
    # Unique Unit Identity
    unit_legal_name = models.CharField(
        _("legal_name_unit_school"),
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        )
    slug = models.SlugField(unique=True)

    trade_name = models.CharField(
        _("trade_name_unit_school"),
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        )

    tax_identification_number = models.CharField(
        max_length=18,  # suficiente para 00.000.000/0000-00
        unique=True,
        verbose_name=_("CNPJ"),
        validators=[
            RegexValidator(
                r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$|^\d{14}$',
                message=_(
                    "Invalid format for CNPJ."
                    "Use 00.000.000/0000-00 ou 00000000000000."),
            ),
            validate_cnpj,
        ],
    )

    foundation_date = models.DateField(
        verbose_name=_("foundation_date"),
        )

    class Meta:
        app_label = 'institutions'
        verbose_name = _("Unit School")
        verbose_name_plural = _("Units Schools")
        ordering = ["trade_name"]
        db_table_comment = "Educational institution units"
